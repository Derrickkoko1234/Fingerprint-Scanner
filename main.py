from pyfingerprint.pyfingerprint import PyFingerprint
import time


def enroll_fingerprint(device_path="/dev/tty.S818", baud_rate=57600):
    try:
        print(f"Trying to connect to {device_path} with baud rate {baud_rate}...")
        f = PyFingerprint(device_path, baud_rate, 0xFFFFFFFF, 0x00000000)

        if not f.verifyPassword():
            raise ValueError("The given fingerprint sensor password is wrong!")

    except Exception as e:
        print("The fingerprint sensor could not be initialized!")
        print("Exception message:", e)
        return

    try:
        print("Waiting for finger...")
        while not f.readImage():
            pass

        f.convertImage(0x01)
        result = f.searchTemplate()
        positionNumber = result[0]

        if positionNumber >= 0:
            print("Fingerprint already exists at position #", positionNumber)
            return

        print("Remove finger...")
        f.waitForFingerUp()
        print("Waiting for the same finger again...")
        while not f.readImage():
            pass

        f.convertImage(0x02)
        if f.compareCharacteristics() == 0:
            raise Exception("Fingers do not match")

        f.createTemplate()
        positionNumber = f.storeTemplate()
        print("Fingerprint enrolled successfully!")
        print("New template position #", positionNumber)

    except Exception as e:
        print("Operation failed!")
        print("Exception message:", e)


if __name__ == "__main__":
    # Try with the default baud rate
    enroll_fingerprint()

    # Try with alternative baud rates if the default doesn't work
    time.sleep(2)
    enroll_fingerprint(baud_rate=115200)
    time.sleep(2)
    enroll_fingerprint(baud_rate=9600)
