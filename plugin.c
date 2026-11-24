#include <gtk/gtk.h>
#include <pi-dlp.h>
#include <pi-buffer.h>
#include <pi-socket.h>
#include <pi-error.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>
extern void jp_init(void);
extern int jp_get_home_file_name(const char *, char *, int);
extern int jp_logf(int, const char *, ...);

void plugin_version(int *major,int *minor) { *major=1; *minor=0; }
int plugin_get_name(char *s,int n) { g_strlcpy(s,"VersaMail 2.6.1",n); return 0; }
int plugin_get_menu_name(char *name, int len)
{
    g_strlcpy(name, "VersaMail", len);
    return 0;
}
int plugin_startup(void *info) { (void)info; jp_init(); return 0; }

static gboolean launch(const char *mode, GPid *pid, int *input, int *output)
{
    char script[4096], state[4096];
    jp_get_home_file_name("plugins/versamail.py",script,sizeof script);
    jp_get_home_file_name("versamail.sqlite",state,sizeof state);
    char *args[]={"python3","-u",script,(char *)mode,state,NULL};
    GError *err=NULL;
    gboolean ok=g_spawn_async_with_pipes(NULL,args,NULL,G_SPAWN_SEARCH_PATH |
        (pid ? G_SPAWN_DO_NOT_REAP_CHILD : 0),NULL,NULL,pid,input,output,NULL,&err);
    if (!ok) { jp_logf(4,"VersaMail: %s\n",err->message); g_error_free(err); }
    return ok;
}
static void edit(GtkButton *b,gpointer data)
{ (void)b; (void)data; launch("edit",NULL,NULL,NULL); }
int plugin_gui(GtkWidget *side,GtkWidget *main,unsigned id)
{
    (void)side; (void)id;
    GtkWidget *button=gtk_button_new_with_label("Manage VersaMail accounts");
    gtk_box_pack_start(GTK_BOX(main),button,FALSE,FALSE,6);
    g_signal_connect(button,"clicked",G_CALLBACK(edit),NULL);
    /* J-Pilot creates a hidden main box each time the plugin is selected. */
    gtk_widget_show_all(main);
    return 0;
}

/* One synchronous DLP operation per line. Keep the live pilot-link socket
   and its protocol state in the J-Pilot process. Binary payloads are base64. */
static void serve(char *line, FILE *reply,int sd,int db,pi_buffer_t *buf)
{
    g_auto(GStrv) a=g_strsplit(g_strchomp(line)," ",6);
    int count=g_strv_length(a), rc=-1, key=count>1 ? atoi(a[1]) : 0;
    int attr=0,cat=0,version=0,total=0;
    recordid_t uid=0;
    size_t len=0;
    unsigned char pref[4096];
    unsigned long creator=0x61736333;
    g_autofree char *encoded=NULL;
    if (!strcmp(a[0],"count")) {
        rc=dlp_ReadOpenDBInfo(sd,db,&total);
        if (rc>=0) { fprintf(reply,"%d\n",total); return; }
    } else if (!strcmp(a[0],"record") && count==2) {
        rc=dlp_ReadRecordByIndex(sd,db,key,buf,&uid,&attr,&cat);
        if (rc>=0) {
            encoded=g_base64_encode(buf->data,buf->used);
            fprintf(reply,"%lu %d %d %s\n",uid,attr,cat,encoded); return;
        }
    } else if (!strcmp(a[0],"pref") && count==2) {
        rc=dlp_ReadAppPreference(sd,creator,key,1,sizeof pref,pref,&len,&version);
        if (rc==PI_ERR_DLP_PALMOS && pi_palmos_error(sd)==dlpErrNotFound) {
            fputs("missing\n",reply); return;
        }
        if (rc>=0 && len<=sizeof pref && version==0x950) {
            encoded=g_base64_encode(pref,len); fprintf(reply,"%s\n",encoded); return;
        }
        rc=-1;
    } else if (!strcmp(a[0],"set") && count==3) {
        g_autofree guchar *bytes=g_base64_decode(a[2],&len);
        rc=dlp_WriteAppPreference(sd,creator,key,1,0x950,bytes,len);
    } else if (!strcmp(a[0],"write") && count==5) {
        g_autofree guchar *bytes=g_base64_decode(a[4],&len);
        rc=dlp_WriteRecord(sd,db,atoi(a[2]),key,atoi(a[3]),bytes,len,&uid);
    } else if (!strcmp(a[0],"log")) {
        jp_logf(4,"VersaMail: %s",line+4); rc=0;
    }
    fprintf(reply,rc<0 ? "error %d\n" : "ok\n",rc);
}
int plugin_sync(int sd)
{
    int db,in,out,status=0;
    GPid pid;
    if (dlp_OpenDB(sd,0,dlpOpenReadWrite,"MultiMail Messages",&db)<0) return -1;
    int result=-1;
    pi_buffer_t *buf=pi_buffer_new(1024);
    if (buf && launch("sync",&pid,&in,&out)) {
        FILE *commands=fdopen(out,"r"), *reply=fdopen(in,"w");
        char *line=NULL; size_t cap=0;
        while (getline(&line,&cap,commands)>=0) {
            serve(line,reply,sd,db,buf);
            if (fflush(reply)) break;
        }
        free(line); fclose(commands); fclose(reply);
        if (waitpid(pid,&status,0)==pid && WIFEXITED(status) && !WEXITSTATUS(status)) result=0;
        g_spawn_close_pid(pid);
    }
    if (buf) pi_buffer_free(buf);
    return dlp_CloseDB(sd,db)<0 ? -1 : result;
}
