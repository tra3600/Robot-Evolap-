"""Pilotage moteur : un correcteur proportionnel recentre le motif suivi dans l'image."""

from abc import ABC, abstractmethod


class MotorDriver(ABC):
    """Interface à implémenter pour le matériel réel (GPIO, série, ...)."""

    @abstractmethod
    def set_speed(self, pan, tilt):
        """pan, tilt dans [-1, 1] ; pan > 0 tourne vers la droite, tilt > 0 vers le bas."""

    def stop(self):
        self.set_speed(0.0, 0.0)


class SimulatedMotor(MotorDriver):
    """Moteur factice : mémorise les commandes (utile en test et sans matériel)."""

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.history = []

    def set_speed(self, pan, tilt):
        self.history.append((pan, tilt))
        if self.verbose:
            print(f"moteur pan={pan:+.2f} tilt={tilt:+.2f}")


class PanTiltController:
    """Convertit l'écart entre le centre du motif et le centre de l'image en commande moteur."""

    def __init__(self, motor, image_width, image_height, gain=1.0, zone_morte=0.05):
        self.motor = motor
        self.w, self.h = image_width, image_height
        self.gain = gain
        self.zone_morte = zone_morte

    def commande(self, centre_motif):
        """Écart normalisé dans [-1, 1] -> vitesses (pan, tilt), nulles dans la zone morte."""
        ex = (centre_motif[0] - self.w / 2) / (self.w / 2)
        ey = (centre_motif[1] - self.h / 2) / (self.h / 2)
        return tuple(0.0 if abs(e) < self.zone_morte else max(-1.0, min(1.0, self.gain * e))
                     for e in (ex, ey))

    def suit(self, centre_motif):
        pan, tilt = self.commande(centre_motif)
        self.motor.set_speed(pan, tilt)
        return pan, tilt
