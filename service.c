#include <stdio.h>
#include <signal.h>
#include <stdlib.h>
#include <systemd/sd-daemon.h>

static sigset_t sig_set;

// http://man7.org/linux/man-pages/man2/sigprocmask.2.html
void static set_new_sig_mask()
{
    sigemptyset(&sig_set);
    
    if (sigaddset(&sig_set, SIGTERM) != 0) {
        fprintf(stderr, "sigaddset failed");
        exit(1);
    }

    if (sigprocmask(SIG_SETMASK, &sig_set, NULL) != 0) {
        fprintf(stderr, "sigprocmask failed");
        exit(2);
    }
}

int main()
{
    set_new_sig_mask();

    sd_notify(0, "READY=1");

    int sig;
    if (sigwait(&sig_set, &sig) != 0) {
        fprintf(stderr, "sigwait failed");
        exit(3);
    }
    printf("Service received Unix signal: %d\n", sig);

    sd_notify(0, "STOPPING=1");

    return 0;
}