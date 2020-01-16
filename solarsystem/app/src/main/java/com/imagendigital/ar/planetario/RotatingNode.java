package com.imagendigital.ar.planetario;

import android.animation.ObjectAnimator;
import android.support.annotation.Nullable;
import android.view.animation.LinearInterpolator;
import com.google.ar.sceneform.FrameTime;
import com.google.ar.sceneform.Node;
import com.google.ar.sceneform.math.Quaternion;
import com.google.ar.sceneform.math.QuaternionEvaluator;
import com.google.ar.sceneform.math.Vector3;

public class RotatingNode extends Node {

  // Usamos una animación para hacer que el nodo tenga rotación
  @Nullable private ObjectAnimator orbitAnimation = null;
  private float degreesPerSecond = 90.0f;

  private final SolarSettings solarSettings;
  private final boolean isOrbit;
  private final boolean clockwise;
  private final float axisTiltDeg;
  private float lastSpeedMultiplier = 1.0f;

  public RotatingNode(
      SolarSettings solarSettings, boolean isOrbit, boolean clockwise, float axisTiltDeg) {
    this.solarSettings = solarSettings;
    this.isOrbit = isOrbit;
    this.clockwise = clockwise;
    this.axisTiltDeg = axisTiltDeg;
  }

  @Override
  public void onUpdate(FrameTime frameTime) {
    super.onUpdate(frameTime);

    // Si la animacion no se ha establecido no hacemos nada
    if (orbitAnimation == null) {
      return;
    }

    // Comprobamos si necesitamos cambiar la velocidad de rotacion
    float speedMultiplier = getSpeedMultiplier();

    // Si no cambia nada, la velocidad de rotacion es la misma
    if (lastSpeedMultiplier == speedMultiplier) {
      return;
    }

    // En caso de que la velocidad sea 0 se para la animacion de la orbita
    // en otro caso se actualiza la velocidad de animacion
    if (speedMultiplier == 0.0f) {
      orbitAnimation.pause();
    } else {
      orbitAnimation.resume();

      float animatedFraction = orbitAnimation.getAnimatedFraction();
      orbitAnimation.setDuration(getAnimationDuration());
      orbitAnimation.setCurrentFraction(animatedFraction);
    }
    lastSpeedMultiplier = speedMultiplier;
  }

  public void setDegreesPerSecond(float degreesPerSecond) {
    this.degreesPerSecond = degreesPerSecond;
  }

  @Override
  public void onActivate() {
    startAnimation();
  }

  @Override
  public void onDeactivate() {
    stopAnimation();
  }

  private long getAnimationDuration() {
    return (long) (1000 * 360 / (degreesPerSecond * getSpeedMultiplier()));
  }

  private float getSpeedMultiplier() {
    if (isOrbit) {
      return solarSettings.getOrbitSpeedMultiplier();
    } else {
      return solarSettings.getRotationSpeedMultiplier();
    }
  }

  // Metodo para comenzar la animacion
  private void startAnimation() {
    if (orbitAnimation != null) {
      return;
    }

    orbitAnimation = createAnimator(clockwise, axisTiltDeg);
    orbitAnimation.setTarget(this);
    orbitAnimation.setDuration(getAnimationDuration());
    orbitAnimation.start();
  }

  // Metodo para parar la animacion
  private void stopAnimation() {
    if (orbitAnimation == null) {
      return;
    }
    orbitAnimation.cancel();
    orbitAnimation = null;
  }

  /** Devuelve un  ObjectAnimator que hace que los nodos roten */
  private static ObjectAnimator createAnimator(boolean clockwise, float axisTiltDeg) {
    // En primer lugar establecemos las orientacions que animaran al circulo
    Quaternion[] orientations = new Quaternion[4];
    // La primera rotacion que se aplica es a los ejes
    Quaternion baseOrientation = Quaternion.axisAngle(new Vector3(1.0f, 0f, 0.0f), axisTiltDeg);
    for (int i = 0; i < orientations.length; i++) {
      float angle = i * 360 / (orientations.length - 1);
      if (clockwise) {
        angle = 360 - angle;
      }
      Quaternion orientation = Quaternion.axisAngle(new Vector3(0.0f, 1.0f, 0.0f), angle);
      orientations[i] = Quaternion.multiply(baseOrientation, orientation);
    }

    ObjectAnimator orbitAnimation = new ObjectAnimator();
    // Se realiza un cast para asegurarnos que la sobrecarga de parametros es correcta
    orbitAnimation.setObjectValues((Object[]) orientations);

    // Next, give it the localRotation property.
    orbitAnimation.setPropertyName("localRotation");

    // Usar el evaluador QuaternionEvaluator de Sceneform.
    orbitAnimation.setEvaluator(new QuaternionEvaluator());

    //  Permite a la variable orbitAnimation a que se repita indefinidamente
    orbitAnimation.setRepeatCount(ObjectAnimator.INFINITE);
    orbitAnimation.setRepeatMode(ObjectAnimator.RESTART);
    orbitAnimation.setInterpolator(new LinearInterpolator());
    orbitAnimation.setAutoCancel(true);

    return orbitAnimation;
  }
}
