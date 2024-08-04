import ctypes
from ctypes import wintypes
import time

# Constants
WINBIO_TYPE_FINGERPRINT = 0x00000008
WINBIO_POOL_SYSTEM = 0x00000001
WINBIO_FLAG_DEFAULT = 0x00000000
WINBIO_BIR_QUALITY = 0x00000010
WINBIO_CAPTURE_PURPOSE_ENROLL = 0x00000001
WINBIO_NO_SUBTYPE_AVAILABLE = 0xFFFFFFFF

# Load the DLL
winbio = ctypes.WinDLL("Winbio.dll")


# Define structures and function prototypes
class WINBIO_SESSION_HANDLE(ctypes.Structure):
    _fields_ = [("handle", wintypes.HANDLE)]


class WINBIO_UNIT_ID(ctypes.Structure):
    _fields_ = [("unit_id", wintypes.ULONG)]


class WINBIO_BIR_DATA(ctypes.Structure):
    _fields_ = [
        ("Size", wintypes.ULONG),
        ("Flags", wintypes.ULONG),
        ("Data", ctypes.POINTER(ctypes.c_ubyte)),
    ]


# Initialize and open a biometric session
def open_session():
    session_handle = WINBIO_SESSION_HANDLE()
    result = winbio.WinBioOpenSession(
        WINBIO_TYPE_FINGERPRINT,
        WINBIO_POOL_SYSTEM,
        WINBIO_FLAG_DEFAULT,
        None,
        0,
        None,
        ctypes.byref(session_handle),
    )
    if result != 0:
        raise Exception(f"Failed to open session: {result}")
    return session_handle


# Capture fingerprint
def capture_fingerprint(session_handle):
    unit_id = WINBIO_UNIT_ID()
    sample = WINBIO_BIR_DATA()
    sub_factor = wintypes.BYTE()

    result = winbio.WinBioCaptureSample(
        session_handle,
        WINBIO_NO_SUBTYPE_AVAILABLE,
        WINBIO_CAPTURE_PURPOSE_ENROLL,
        ctypes.byref(unit_id),
        ctypes.byref(sample),
        ctypes.byref(sub_factor),
        None,
    )
    if result != 0:
        raise Exception(f"Failed to capture sample: {result}")
    return sample


# Close the session
def close_session(session_handle):
    result = winbio.WinBioCloseSession(session_handle)
    if result != 0:
        raise Exception(f"Failed to close session: {result}")


# Main function
if __name__ == "__main__":
    try:
        print("Opening biometric session...")
        session_handle = open_session()

        print("Capturing fingerprint...")
        fingerprint = capture_fingerprint(session_handle)
        print("Fingerprint captured successfully!")

        # You can now use the fingerprint data for enrollment or verification
        # For demonstration, we just print the size of the captured data
        print(f"Captured fingerprint data size: {fingerprint.Size}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        print("Closing biometric session...")
        close_session(session_handle)
