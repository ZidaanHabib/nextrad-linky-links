import pytest
from helpers.controller_helper_functions import ControllerMath
import os

#def main():

source_lat, source_long = -33.908109924189084, 18.395487481680284  # Twin towers

def test_dist_az1():
    target_lat1, target_long1 = -33.90831103255768, 18.403917702960676  # Cushty neighbourhood deli
    distance = ControllerMath.haversine(source_lat, source_long, target_lat1, target_long1)
    az = ControllerMath.determine_azimuth_difference(source_lat, source_long, target_lat1, target_long1)
    assert 770 < distance < 780
    assert 91 < az < 92

def test_dist_az2():
    target_lat, target_long = -33.908470921022904, 18.394677458542322  # COsta del sol
    distance = ControllerMath.haversine(source_lat, source_long, target_lat, target_long)
    az = ControllerMath.determine_azimuth_difference(source_lat, source_long, target_lat, target_long)
    assert 78 < distance < 85
    assert 241 < az < 242

def test_dist_az3():
    target_lat, target_long = -33.90625351007551, 18.394488341295258
    distance = ControllerMath.haversine(source_lat, source_long, target_lat, target_long)
    az = ControllerMath.determine_azimuth_difference(source_lat, source_long, target_lat, target_long)
    assert 226 < distance < 232
    assert 335.5 < az < 336.5

def test_dist_az4():
    target_lat, target_long = -33.904649621727714, 18.39800321367718
    distance = ControllerMath.haversine(source_lat, source_long, target_lat, target_long)
    az = ControllerMath.determine_azimuth_difference(source_lat, source_long, target_lat, target_long)
    assert 445 < distance < 452
    assert 30.5 < az < 31.5

def test_dist_az5():
    target_lat, target_long = -33.91740689264841, 18.403830195032505  # signal hill
    distance = ControllerMath.haversine(source_lat, source_long, target_lat, target_long)
    az = ControllerMath.determine_azimuth_difference(source_lat, source_long, target_lat, target_long)
    assert 1280 < distance < 1290
    assert 143 < az < 144

def test_el1():
    source_alt = 2
    target_alt = 0
    dist = 2
    el = ControllerMath.determine_elevation_difference(source_alt, target_alt, dist)
    assert el == 45

def test_el2():
    source_alt = 4
    target_alt = 0
    dist = 2
    el = ControllerMath.determine_elevation_difference(source_alt, target_alt, dist)
    assert el == 63.43

def test_el3():
    source_alt = 100
    target_alt = 88.5
    dist = 200
    el = ControllerMath.determine_elevation_difference(source_alt, target_alt, dist)
    assert el == 3.29

def test_el3():
    source_alt = 20
    target_alt = 20
    dist = 200
    el = ControllerMath.determine_elevation_difference(source_alt, target_alt, dist)
    assert el == 0

def test_el4():
    source_alt = 0
    target_alt = 2
    dist = 2
    el = ControllerMath.determine_elevation_difference(source_alt, target_alt, dist)
    assert el == -45

