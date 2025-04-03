import syscallgrouper as sg
import json


def hacker_syscallgroup() -> sg.SyscallGroup:
    hacker_raw = """
{
  "pids": 8,
  "syscalls": {
    "read": 404,
    "write": 12,
    "execve": 7,
    "brk": 22,
    "access": 19,
    "openat": 723,
    "fstat": 326,
    "mmap": 118,
    "close": 654,
    "pread64": 14,
    "arch_prctl": 7,
    "set_tid_address": 7,
    "set_robust_list": 8,
    "rseq": 7,
    "mprotect": 34,
    "prlimit64": 8,
    "munmap": 13,
    "getrandom": 8,
    "getuid": 14,
    "getgid": 14,
    "geteuid": 15,
    "getegid": 14,
    "rt_sigprocmask": 80,
    "ioctl": 12,
    "rt_sigaction": 44,
    "uname": 2,
    "getcwd": 1,
    "getpid": 4,
    "getppid": 3,
    "newfstatat": 62,
    "lseek": 24,
    "getpgrp": 1,
    "fcntl": 8,
    "clone": 3,
    "prctl": 24,
    "getdents64": 40,
    "wait4": 6,
    "rt_sigreturn": 6,
    "futex": 6,
    "socket": 20,
    "connect": 20,
    "epoll_create1": 18,
    "timerfd_create": 18,
    "epoll_ctl": 108,
    "timerfd_settime": 18,
    "epoll_pwait2": 72,
    "sendto": 19,
    "recvfrom": 24,
    "statx": 180,
    "getgroups": 2,
    "epoll_wait": 4,
    "dup2": 2,
    "ppoll": 1,
    "setsockopt": 2,
    "pselect6": 1,
    "getsockopt": 1,
    "shutdown": 1,
    "fadvise64": 1
  },
  "read": {
    "0<pipe:[2670257]>": 196,
    "3</usr/lib/libreadline.so.8.2>": 1,
    "3</usr/lib/libc.so.6>": 7,
    "3</usr/lib/libncursesw.so.6.5>": 1,
    "3</etc/nsswitch.conf>": 8,
    "3</etc/passwd>": 5,
    "3</usr/lib/libcap.so.2.75>": 4,
    "3</etc/group>": 18,
    "3</usr/lib/libnss_systemd.so.2>": 1,
    "3</usr/lib/libm.so.6>": 2,
    "3</usr/lib/libgcc_s.so.1>": 2,
    "3</proc/sys/kernel/random/boot_id>": 2,
    "3</etc/host.conf>": 2,
    "3</etc/resolv.conf>": 2,
    "3</usr/lib/libnss_mymachines.so.2>": 1,
    "3</usr/lib/libnss_resolve.so.2>": 1,
    "3</etc/services>": 150,
    "3<socket:[2673771>": 1
  },
  "write": {
    "1</dev/pts/4>": 11,
    "1</home/bummie/projects/AAUGrader/hackfile.txt>": 1
  }
}"""

    group = sg.SyscallGroup()
    group.from_json(hacker_raw)
    return group


def normal_syscallgroup() -> sg.SyscallGroup:
    normal_raw = """
        {
  "pids": 3,
  "syscalls": {
    "execve": 3,
    "brk": 12,
    "mmap2": 8,
    "access": 8,
    "openat": 20,
    "statx": 2,
    "close": 23,
    "read": 21,
    "set_thread_area": 1,
    "set_tid_address": 4,
    "set_robust_list": 4,
    "rseq": 4,
    "mprotect": 16,
    "ugetrlimit": 3,
    "munmap": 6,
    "write": 22,
    "getrandom": 4,
    "pipe2": 1,
    "rt_sigprocmask": 12,
    "dup2": 1,
    "fcntl64": 1,
    "fstat": 17,
    "mmap": 48,
    "pread64": 6,
    "arch_prctl": 3,
    "prlimit64": 5,
    "futex": 2,
    "getuid": 6,
    "getgid": 6,
    "geteuid": 6,
    "getegid": 6,
    "rt_sigaction": 34,
    "uname": 2,
    "newfstatat": 28,
    "getpid": 6,
    "getppid": 6,
    "getpgrp": 2,
    "ioctl": 4,
    "fadvise64": 1,
    "wait4": 1
  },
  "read": {
    "3</usr/lib32/libc.so.6>": 1,
    "0</dev/pts/5>": 11,
    "3</usr/lib/libreadline.so.8.2>": 2,
    "3</usr/lib/libc.so.6>": 3,
    "3</usr/lib/libncursesw.so.6.5>": 2,
    "3</home/bummie/projects/AAUGrader/grades.txt>": 2
  },
  "write": {
    "1</dev/pts/5>": 21,
    "1<pipe:[2590041>": 1
  }
}
    """
    group = sg.SyscallGroup()
    group.from_json(normal_raw)
    return group


def normal_unknown_user_syscallgroup() -> sg.SyscallGroup:
    normal_raw = """
        {
  "pids": 3,
  "syscalls": {
    "execve": 3,
    "brk": 12,
    "mmap2": 8,
    "access": 7,
    "openat": 19,
    "statx": 2,
    "close": 21,
    "read": 17,
    "set_thread_area": 1,
    "set_tid_address": 4,
    "set_robust_list": 4,
    "rseq": 4,
    "mprotect": 16,
    "ugetrlimit": 3,
    "munmap": 5,
    "write": 18,
    "getrandom": 4,
    "pipe2": 1,
    "rt_sigprocmask": 12,
    "dup2": 1,
    "makedev": 1,
    "mmap": 48,
    "fstat": 16,
    "pread64": 6,
    "arch_prctl": 3,
    "prlimit64": 5,
    "futex": 2,
    "getuid": 6,
    "getgid": 6,
    "geteuid": 6,
    "getegid": 6,
    "rt_sigaction": 34,
    "uname": 2,
    "newfstatat": 28,
    "getpid": 6,
    "getppid": 6,
    "getpgrp": 2,
    "ioctl": 4,
    "fadvise64": 1
  },
  "read": {
    "3</usr/lib32/libc.so.6>": 1,
    "0</dev/pts/5>": 7,
    "3</usr/lib/libreadline.so.8.2>": 2,
    "3</usr/lib/libc.so.6>": 3,
    "3</usr/lib/libncursesw.so.6.5>": 2,
    "3</home/bummie/projects/AAUGrader/grades.txt>": 2
  },
  "write": {
    "1</dev/pts/5>": 17,
    "1<pipe:[2588162>": 1
  }
}
    """
    group = sg.SyscallGroup()
    group.from_json(normal_raw)
    return group


def test_sum():
    assert sum([1, 2, 3]) == 6, "Should be 6"


def test_scoring():
    hg = hacker_syscallgroup()
    ng = normal_syscallgroup()
    nug = normal_unknown_user_syscallgroup()

    nug.calculate_malicious_score(ng)
    print(f"Normal: {nug.score}")

    hg.calculate_malicious_score(ng)
    print(f"Hacker: {hg.score}")
    assert hg.score > 0


if __name__ == "__main__":
    test_sum()
    test_scoring()

    print("Everything passed")
