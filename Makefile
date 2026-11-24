CC ?= cc
CFLAGS ?= -O2 -g
PROFILE ?= $(if $(JPILOT_HOME),$(JPILOT_HOME),$(HOME))/.jpilot
PLUGIN = libjpilot-versamail.so
all: $(PLUGIN)
$(PLUGIN): plugin.c
	$(CC) $(CPPFLAGS) $(CFLAGS) -Wall -Wextra -shared -fPIC -o $@ $< $(shell pkg-config --cflags --libs gtk+-3.0 gio-unix-2.0) -lpisock $(LDFLAGS)
install: all
	install -d "$(PROFILE)/plugins"
	install -m644 $(PLUGIN) versamail.py "$(PROFILE)/plugins"
clean:
	$(RM) $(PLUGIN)
.PHONY: all install clean
