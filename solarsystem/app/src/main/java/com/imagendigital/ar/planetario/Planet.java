package com.imagendigital.ar.planetario;

import android.content.Context;
import android.view.MotionEvent;
import android.widget.TextView;
import com.google.ar.sceneform.FrameTime;
import com.google.ar.sceneform.HitTestResult;
import com.google.ar.sceneform.Node;
import com.google.ar.sceneform.math.Quaternion;
import com.google.ar.sceneform.math.Vector3;
import com.google.ar.sceneform.rendering.ModelRenderable;
import com.google.ar.sceneform.rendering.ViewRenderable;
import com.imagendigital.ar.planetario.R;

// Node representa un planeta
public class Planet extends Node implements Node.OnTapListener {

  // Atributos del planeta
  private final String planetName;
  private final float planetScale;
  private final float orbitDegreesPerSecond;
  private final float axisTilt;
  private final ModelRenderable planetRenderable;
  private final SolarSettings solarSettings;

  // Informacion del planeta
  private Node infoCard;

  // Visual del planeta
  private RotatingNode planetVisual;
  private final Context context;

  private static final float INFO_CARD_Y_POS_COEFF = 0.55f;

  public Planet(
      Context context,
      String planetName,
      float planetScale,
      float orbitDegreesPerSecond,
      float axisTilt,
      ModelRenderable planetRenderable,
      SolarSettings solarSettings) {
    this.context = context;
    this.planetName = planetName;
    this.planetScale = planetScale;
    this.orbitDegreesPerSecond = orbitDegreesPerSecond;
    this.axisTilt = axisTilt;
    this.planetRenderable = planetRenderable;
    this.solarSettings = solarSettings;
    setOnTapListener(this);
  }

  @Override
  @SuppressWarnings({"AndroidApiChecker", "FutureReturnValueIgnored"})
  public void onActivate() {

    if (getScene() == null) {
      throw new IllegalStateException("¡La escena está vacia!");
    }

    if (infoCard == null) {
      infoCard = new Node();
      infoCard.setParent(this);
      infoCard.setEnabled(false);
      infoCard.setLocalPosition(new Vector3(0.0f, planetScale * INFO_CARD_Y_POS_COEFF, 0.0f));

      ViewRenderable.builder()
          .setView(context, R.layout.planet_card_view)
          .build()
          .thenAccept(
              (renderable) -> {
                infoCard.setRenderable(renderable);
                TextView textView = (TextView) renderable.getView();
                textView.setText(planetName);
              })
          .exceptionally(
              (throwable) -> {
                throw new AssertionError("No es posible cargar la tarjeta de informacion", throwable);
              });
    }

    if (planetVisual == null) {
      // Creamos un contador de rotaciones que permite manteres la orientacion independientemente de la orbita
      RotatingNode counterOrbit = new RotatingNode(solarSettings, true, true, 0f);
      counterOrbit.setDegreesPerSecond(orbitDegreesPerSecond);
      counterOrbit.setParent(this);

      planetVisual = new RotatingNode(solarSettings, false, false, axisTilt);
      planetVisual.setParent(counterOrbit);
      planetVisual.setRenderable(planetRenderable);
      planetVisual.setLocalScale(new Vector3(planetScale, planetScale, planetScale));
    }
  }

  @Override
  public void onTap(HitTestResult hitTestResult, MotionEvent motionEvent) {
    if (infoCard == null) {
      return;
    }

    infoCard.setEnabled(!infoCard.isEnabled());
  }

  @Override
  public void onUpdate(FrameTime frameTime) {
    if (infoCard == null) {
      return;
    }
    
    if (getScene() == null) {
      return;
    }
    Vector3 cameraPosition = getScene().getCamera().getWorldPosition();
    Vector3 cardPosition = infoCard.getWorldPosition();
    Vector3 direction = Vector3.subtract(cameraPosition, cardPosition);
    Quaternion lookRotation = Quaternion.lookRotation(direction, Vector3.up());
    infoCard.setWorldRotation(lookRotation);
  }
}
