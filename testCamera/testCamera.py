#Author- James Adams
#Description- Testing simplified rotation

import adsk.core, adsk.fusion, adsk.cam, traceback, math

framesPerRotation = 12
numRotations = 1
rotationDirection = -1
numFrames = int(abs(framesPerRotation * numRotations))


def rotateAroundZAxis(camera, radianAngle):
    eye = camera.eye
    cos = math.cos(radianAngle)
    sin = math.sin(radianAngle)

    camera.eye = adsk.core.Point3D.create(eye.x * cos - eye.y * sin, 
                                          eye.x * sin + eye.y * cos, 
                                          eye.z)
    # Set camera property to trigger update.
    camera.upVector = adsk.core.Vector3D.create(0, 0, 1)
    return camera

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        # Get the viewport.
        viewport = app.activeViewport
        camera = viewport.camera
        cameraOffset = camera.target.vectorTo(camera.eye)

        # one extra to end back at the starting point
        for i in range(0, numFrames+1):

            offset = camera.target.copy()
            offset.translateBy(cameraOffset)
            camera.eye = offset

            # Rotate camera around axis.
            # If rotation direction is negative, rotate in the opposite direction
            radianAngle = math.pi * 2.0 * i / framesPerRotation * rotationDirection

            viewport.camera = rotateAroundZAxis(camera, radianAngle)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))





