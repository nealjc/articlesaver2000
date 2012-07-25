"""
Detect proxy settings in a platform-independent way
"""

import platform


def get_windows_proxy():
    import win32
    #can get this from registry. how does it differentiate proxies for 
    #different protocols?
    pass


def get_linux_proxy():
    #requests uses HTTP_PROXY etc environment variables...
    pass


def get_proxy():
    """Return a dictionary of proxies for each protocol
    e.g. 
    {"http":"http://10.1.1.1:8080",
     "https":http://10.1.1.1.:8081
    }

    The dictionary may be empty if no proxy was found
    """
    if platform.system() == 'Windows':
        return get_windows_proxy()
    else:
        return get_linux_proxy()

