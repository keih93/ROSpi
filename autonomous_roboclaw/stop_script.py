import Engine
import time
import camera_module

def main():
    #engine = Engine.Engine()
    camera = camera_module.CameraModule()
    #time.sleep(1)
    #engine.stop_all_wheels()
    print (camera.getDirection())

if __name__ == '__main__':
    main()
