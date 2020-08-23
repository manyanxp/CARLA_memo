#!/usr/bin/env python

# Copyright (c) 2019 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

try:
    import pygame
except ImportError:
    raise RuntimeError('cannot import pygame, make sure pygame package is installed')

try:
    import numpy as np
except ImportError:
    raise RuntimeError('cannot import numpy, make sure numpy package is installed')

try:
    import queue
except ImportError:
    import Queue as queue

import carla

import math
import random

try:
    import pygame
    from pygame.locals import KMOD_CTRL
    from pygame.locals import KMOD_SHIFT
    from pygame.locals import K_0
    from pygame.locals import K_9
    from pygame.locals import K_BACKQUOTE
    from pygame.locals import K_BACKSPACE
    from pygame.locals import K_COMMA
    from pygame.locals import K_DOWN
    from pygame.locals import K_ESCAPE
    from pygame.locals import K_F1
    from pygame.locals import K_LEFT
    from pygame.locals import K_PERIOD
    from pygame.locals import K_RIGHT
    from pygame.locals import K_SLASH
    from pygame.locals import K_SPACE
    from pygame.locals import K_TAB
    from pygame.locals import K_UP
    from pygame.locals import K_a
    from pygame.locals import K_c
    from pygame.locals import K_g
    from pygame.locals import K_d
    from pygame.locals import K_h
    from pygame.locals import K_m
    from pygame.locals import K_n
    from pygame.locals import K_p
    from pygame.locals import K_q
    from pygame.locals import K_r
    from pygame.locals import K_s
    from pygame.locals import K_w
    from pygame.locals import K_l
    from pygame.locals import K_i
    from pygame.locals import K_z
    from pygame.locals import K_x
    from pygame.locals import K_MINUS
    from pygame.locals import K_EQUALS
except ImportError:
    raise RuntimeError('cannot import pygame, make sure pygame package is installed')

class CarlaSyncMode(object):
    """
    Context manager to synchronize output from different sensors. Synchronous
    mode is enabled as long as we are inside this context

        with CarlaSyncMode(world, sensors) as sync_mode:
            while True:
                data = sync_mode.tick(timeout=1.0)

    """

    def __init__(self, world, *sensors, **kwargs):
        self.world = world
        self.sensors = sensors
        self.frame = None
        self.delta_seconds = 1.0 / kwargs.get('fps', 20)
        self._queues = []
        self._settings = None

    def __enter__(self):
        self._settings = self.world.get_settings()
        self.frame = self.world.apply_settings(carla.WorldSettings(
            no_rendering_mode=False,
            synchronous_mode=True,
            fixed_delta_seconds=self.delta_seconds))

        def make_queue(register_event):
            q = queue.Queue()
            register_event(q.put)
            self._queues.append(q)

        make_queue(self.world.on_tick)
        for sensor in self.sensors:
            make_queue(sensor.listen)
        return self

    def tick(self, timeout):
        self.frame = self.world.tick()
        data = [self._retrieve_data(q, timeout) for q in self._queues]
        assert all(x.frame == self.frame for x in data)
        return data

    def __exit__(self, *args, **kwargs):
        self.world.apply_settings(self._settings)

    def _retrieve_data(self, sensor_queue, timeout):
        while True:
            data = sensor_queue.get(timeout=timeout)
            if data.frame == self.frame:
                return data

def get_font():
    fonts = [x for x in pygame.font.get_fonts()]
    default_font = 'ubuntumono'
    font = default_font if default_font in fonts else fonts[0]
    font = pygame.font.match_font(font)
    return pygame.font.Font(font, 14)

def get_transform(vehicle_location, angle, d=6.4):
    a = math.radians(angle)
    location = carla.Location(d * math.cos(a), d * math.sin(a), 2.0) + vehicle_location
    return carla.Transform(location, carla.Rotation(yaw=180 + angle, pitch=-15))

def draw_image(surface, image, blend=False):
    array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
    array = np.reshape(array, (image.height, image.width, 4))
    array = array[:, :, :3]
    array = array[:, :, ::-1]
    image_surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))
    if blend:
        image_surface.set_alpha(100)
    surface.blit(image_surface, (0, 0))

def key_left(vehicle):
    tf = vehicle.get_transform()
    print('左 before yaw {}'.format(tf.rotation.yaw))
    tf.rotation.yaw = tf.rotation.yaw - 1
    vehicle.set_transform(tf)
    print('左 after yaw {}'.format(tf.rotation.yaw))

def key_right(vehicle):
    tf = vehicle.get_transform()
    print('右 before yaw {}'.format(tf.rotation.yaw))
    tf.rotation.yaw = tf.rotation.yaw + 1
    vehicle.set_transform(tf)
    print('右 after yaw {}'.format(tf.rotation.yaw))

def draw_arrow_ext(debug, src):
    dest_x = src + carla.Location(x=5)
    dest_y = src + carla.Location(y=5)
    dest_z = src + carla.Location(z=5)
    debug.draw_arrow(src, dest_x, color=carla.Color(255,0,0),life_time=0)
    debug.draw_arrow(src, dest_y, color=carla.Color(0,255,0),life_time=0)
    debug.draw_arrow(src, dest_z, color=carla.Color(0,0,255),life_time=0)

def get_traffic_lights(world):
    traffic_lights = []
    for actor in world.get_actors():
        print(actor.type_id)
        if actor.type_id == 'traffic.traffic_light':
            traffic_lights.append(actor)

    return traffic_lights

import math
import time
import numpy as np

def get_angle_radian(l1, l2):
    return math.atan2(l2.y - l1.y, l2.x - l1.x)
        
def draw_line(debug, src, dest, color=carla.Color(0, 255, 0), lt=-1.0):
    src = src + carla.Location(z=0.25)
    dest = dest + carla.Location(z=0.25)

    debug.draw_line(src, dest, color=color, life_time=lt)

def should_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                return True
    return False

def main():

    pygame.init()

    display = pygame.display.set_mode(
        (800, 600),
        pygame.HWSURFACE | pygame.DOUBLEBUF)
    font = get_font()
    clock = pygame.time.Clock()


    try:
        actor_list = []

        client = carla.Client('localhost', 2000)
        client.set_timeout(20.0)
        world = client.get_world()
                
        m = world.get_map()
        blueprint_library = world.get_blueprint_library()

        # 開始ポジション
        #start_pose = random.choice(m.get_spawn_points())
        start_pose = carla.Transform(carla.Location(x=(12495.010742/100), y=(-13209.476562/100), z=(830.559692/100)), carla.Rotation(pitch=0.0, yaw=1.227265, roll=0.0))

        # 車両の生成
        vehicle = world.spawn_actor(
            random.choice(blueprint_library.filter('vehicle.mini.cooperst*')),
            start_pose)
        actor_list.append(vehicle)

        camera_rgb = world.spawn_actor(
            blueprint_library.find('sensor.camera.rgb'),
            carla.Transform(carla.Location(x=-5.5, z=2.8), carla.Rotation(pitch=-15)),
            attach_to=vehicle)
        actor_list.append(camera_rgb)

        draw_arrow_ext(world.debug, vehicle.get_location())

        traffic_lights = get_traffic_lights(world)

        current_w = m.get_waypoint(vehicle.get_location(), lane_type=(carla.LaneType.Driving))
       
        waypoint_separation = 1

        with CarlaSyncMode(world, camera_rgb, fps=21) as sync_mode:
            tf = vehicle.get_transform()
            print('initial yaw {}'.format(tf.rotation.yaw))

            while True:
                if should_quit():
                    return
                clock.tick()

                # Advance the simulation and wait for the data.
                snapshot, image_rgb = sync_mode.tick(timeout=2.0)

                #for event in pygame.event.get():
                #    if event.type == pygame.QUIT:
                #        pygame.quit()
                #        sys.exit()
                #    if event.type == pygame.KEYDOWN:  # キーを押したとき
                #        if event.key == K_LEFT:
                #            key_left(vehicle)
                #        if event.key == K_RIGHT:
                #            key_right(vehicle)
                #        # ESCキーならスクリプトを終了
                #        if event.key == K_ESCAPE:
                #            pygame.quit()
                #            sys.exit()
                #        
                #        else:
                #            print("押されたキー = " + pygame.key.name(event.key))
                #    pygame.display.update()
                potential_w = list(current_w.next(waypoint_separation))
                next_w = random.choice(potential_w)

                vehicle.set_transform(next_w.transform)

                potential_w.remove(next_w)

                for traffic_light in traffic_lights:
                    r = get_angle_radian(vehicle.get_location(), traffic_light.get_location()) - math.radians(vehicle.get_transform().rotation.yaw)
                    distance = vehicle.get_location().distance(traffic_light.get_location())
                    #print('id {} r {} distance {}'.format(traffic_light.id, r, distance))

                    while r >= np.pi: r -= 2*np.pi
                    while r < -np.pi: r += 2*np.pi
                    if r > -0.8 and r < 0.8 and distance <= 50:
                        world.debug.draw_box(carla.BoundingBox(traffic_light.get_transform().location,carla.Vector3D(0.5, 0.5, 2)),traffic_light.get_transform().rotation, 0.05, carla.Color(255, 0, 0, 0),0)
                        draw_line(world.debug, vehicle.get_location(), traffic_light.get_location(), color=carla.Color(255, 0, 0), lt=0.01)
                    #else:
                    #    draw_line(world.debug, vehicle.get_location(), traffic_light.get_location(), lt=0)
                
                current_w = next_w

                fps = round(1.0 / snapshot.timestamp.delta_seconds)

                draw_image(display, image_rgb)

                pygame.display.flip()

                time.sleep(0.2)

    finally:
        print('destroying actors.')
        for actor in actor_list:
            actor.destroy()

        pygame.quit()
        print('done.')

if __name__ == '__main__':

    main()
