
package com.imagendigital.ar.planetario;

import android.net.Uri;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.view.GestureDetector;
import android.view.MotionEvent;
import android.view.View;
import android.view.WindowManager;
import android.widget.SeekBar;
import android.widget.Toast;
import com.google.ar.core.Anchor;
import com.google.ar.core.Config;
import com.google.ar.core.Frame;
import com.google.ar.core.HitResult;
import com.google.ar.core.Plane;
import com.google.ar.core.Session;
import com.google.ar.core.Trackable;
import com.google.ar.core.TrackingState;
import com.google.ar.core.exceptions.CameraNotAvailableException;
import com.google.ar.core.exceptions.UnavailableException;
import com.google.ar.sceneform.AnchorNode;
import com.google.ar.sceneform.ArSceneView;
import com.google.ar.sceneform.HitTestResult;
import com.google.ar.sceneform.Node;
import com.google.ar.sceneform.math.Vector3;
import com.google.ar.sceneform.rendering.ModelRenderable;
import com.google.ar.sceneform.rendering.ViewRenderable;
import com.imagendigital.ar.planetario.R;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;

/**
 * Vamos a utilizar las APIs de ARCore y Sceneform
 */
public class SolarActivity extends AppCompatActivity {
  
  // Permiso asociado a la cámara
  private static final int RC_PERMISSIONS = 0x123;
  // Para comprobar si los permisos se han aceptado
  private boolean cameraPermissionRequested;

  // Detector de gestos
  private GestureDetector gestureDetector;

  // Mensaje para cargar los datos
  private Snackbar loadingMessageSnackbar = null;

  // Escena de AR donde se dibujaran los modelos
  private ArSceneView arSceneView;

  // Todos los modelos que se van a utilizar, los planetas
  private ModelRenderable sunRenderable;
  private ModelRenderable mercuryRenderable;
  private ModelRenderable venusRenderable;
  private ModelRenderable earthRenderable;
  private ModelRenderable lunaRenderable;
  private ModelRenderable marsRenderable;
  private ModelRenderable jupiterRenderable;
  private ModelRenderable saturnRenderable;
  private ModelRenderable uranusRenderable;
  private ModelRenderable neptuneRenderable;
  private ViewRenderable solarControlsRenderable;

  // Ajustes del sistema solar
  private final SolarSettings solarSettings = new SolarSettings();

  // Bandera para comprobar si la escena ha sido cargada correctamente
  private boolean hasFinishedLoading = false;

  // Bandera para comprobar si la escena ha sido colocada correctamente
  private boolean hasPlacedSolarSystem = false;

  // Unidad astronómica para calcular el radio. Se utiliza para el posicionamiento del sistema solar
  private static final float AU_TO_METERS = 0.5f;

  @Override
  @SuppressWarnings({"AndroidApiChecker", "FutureReturnValueIgnored"})
  // CompletableFuture requiere un nivel de API superior a 24
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);

    if (!DemoUtils.checkIsSupportedDeviceOrFinish(this)) {
      // En caso de no encontrarnos en un dispositivo compatible se termina la ejecución.
      return;
    }

    // Cargamos la disposión de la escena
    setContentView(R.layout.activity_solar);
    arSceneView = findViewById(R.id.ar_scene_view);

    // Construimos todos los modelos de los planetas
    CompletableFuture<ModelRenderable> sunStage =
        ModelRenderable.builder().setSource(this, Uri.parse("Sol.sfb")).build();
    CompletableFuture<ModelRenderable> mercuryStage =
        ModelRenderable.builder().setSource(this, Uri.parse("Mercury.sfb")).build();
    CompletableFuture<ModelRenderable> venusStage =
        ModelRenderable.builder().setSource(this, Uri.parse("Venus.sfb")).build();
    CompletableFuture<ModelRenderable> earthStage =
        ModelRenderable.builder().setSource(this, Uri.parse("Earth.sfb")).build();
    CompletableFuture<ModelRenderable> lunaStage =
        ModelRenderable.builder().setSource(this, Uri.parse("Luna.sfb")).build();
    CompletableFuture<ModelRenderable> marsStage =
        ModelRenderable.builder().setSource(this, Uri.parse("Mars.sfb")).build();
    CompletableFuture<ModelRenderable> jupiterStage =
        ModelRenderable.builder().setSource(this, Uri.parse("Jupiter.sfb")).build();
    CompletableFuture<ModelRenderable> saturnStage =
        ModelRenderable.builder().setSource(this, Uri.parse("Saturn.sfb")).build();
    CompletableFuture<ModelRenderable> uranusStage =
        ModelRenderable.builder().setSource(this, Uri.parse("Uranus.sfb")).build();
    CompletableFuture<ModelRenderable> neptuneStage =
        ModelRenderable.builder().setSource(this, Uri.parse("Neptune.sfb")).build();

    // Construimos una vista renderizable desde una vista en 2D
    CompletableFuture<ViewRenderable> solarControlsStage =
        ViewRenderable.builder().setView(this, R.layout.solar_controls).build();

    CompletableFuture.allOf(
            sunStage,
            mercuryStage,
            venusStage,
            earthStage,
            lunaStage,
            marsStage,
            jupiterStage,
            saturnStage,
            uranusStage,
            neptuneStage,
            solarControlsStage)
        .handle(
            (notUsed, throwable) -> {
              if (throwable != null) {
                DemoUtils.displayError(this, "No ha sido posible cargar los modelos", throwable);
                return null;
              }

              try {
                sunRenderable = sunStage.get();
                mercuryRenderable = mercuryStage.get();
                venusRenderable = venusStage.get();
                earthRenderable = earthStage.get();
                lunaRenderable = lunaStage.get();
                marsRenderable = marsStage.get();
                jupiterRenderable = jupiterStage.get();
                saturnRenderable = saturnStage.get();
                uranusRenderable = uranusStage.get();
                neptuneRenderable = neptuneStage.get();
                solarControlsRenderable = solarControlsStage.get();

                // Cuando se han terminado de cargar todos los modelos se activa la bandera
                hasFinishedLoading = true;

              } catch (InterruptedException | ExecutionException ex) {
                DemoUtils.displayError(this, "No ha sido posible cargar los modelos", ex);
              }

              return null;
            });

    // Detector de gestos para detectar cuando el usuario pulsa en la pantalla
    gestureDetector =
        new GestureDetector(
            this,
            new GestureDetector.SimpleOnGestureListener() {
              @Override
              public boolean onSingleTapUp(MotionEvent e) {
                onSingleTap(e);
                return true;
              }

              @Override
              public boolean onDown(MotionEvent e) {
                return true;
              }
            });

    // Iniciamos el listener en la escena para que escuche cuando se toque la pantalla
    arSceneView
        .getScene()
        .setOnTouchListener(
            (HitTestResult hitTestResult, MotionEvent event) -> {
              // En caso de que el sistema solar no se haya dibujado, detectamos un toque en la pantalla
              // y comprobamos si se ha realizado el toque en la escena de ARCore para establecer el sistema
              if (!hasPlacedSolarSystem) {
                return gestureDetector.onTouchEvent(event);
              }

              // En otro caso se devuelve false para que el toque se muestre en la escena
              return false;
            });

    // Establecemos un listener de actualización en la escena que esconda el mensaje de carga cuando se ha detectado el plano
    arSceneView
        .getScene()
        .addOnUpdateListener(
            frameTime -> {
              if (loadingMessageSnackbar == null) {
                return;
              }

              Frame frame = arSceneView.getArFrame();
              if (frame == null) {
                return;
              }

              if (frame.getCamera().getTrackingState() != TrackingState.TRACKING) {
                return;
              }

              for (Plane plane : frame.getUpdatedTrackables(Plane.class)) {
                if (plane.getTrackingState() == TrackingState.TRACKING) {
                  hideLoadingMessage();
                }
              }
            });

    // Por último se solicitan permisos para utilizar la camara que es necesaria para utilizar ARCore
    DemoUtils.requestCameraPermission(this, RC_PERMISSIONS);
  }

  @Override
  protected void onResume() {
    super.onResume();
    if (arSceneView == null) {
      return;
    }

    if (arSceneView.getSession() == null) {
      // Si no se ha creado la sesion previamente no se deja de renderizar
      // En casos que ARCore se tenga que actualizar o no se hayan dado los permisos necesarios
      try {
        Config.LightEstimationMode lightEstimationMode =
            Config.LightEstimationMode.ENVIRONMENTAL_HDR;
        Session session =
            cameraPermissionRequested
                ? DemoUtils.createArSessionWithInstallRequest(this, lightEstimationMode)
                : DemoUtils.createArSessionNoInstallRequest(this, lightEstimationMode);
        if (session == null) {
          cameraPermissionRequested = DemoUtils.hasCameraPermission(this);
          return;
        } else {
          arSceneView.setupSession(session);
        }
      } catch (UnavailableException e) {
        DemoUtils.handleSessionException(this, e);
      }
    }

    try {
      arSceneView.resume();
    } catch (CameraNotAvailableException ex) {
      DemoUtils.displayError(this, "Ha sido imposible utilizar la camara", ex);
      finish();
      return;
    }

    if (arSceneView.getSession() != null) {
      showLoadingMessage();
    }
  }

  @Override
  public void onPause() {
    super.onPause();
    if (arSceneView != null) {
      arSceneView.pause();
    }
  }

  @Override
  public void onDestroy() {
    super.onDestroy();
    if (arSceneView != null) {
      arSceneView.destroy();
    }
  }

  @Override
  public void onRequestPermissionsResult(
      int requestCode, @NonNull String[] permissions, @NonNull int[] results) {
    if (!DemoUtils.hasCameraPermission(this)) {
      if (!DemoUtils.shouldShowRequestPermissionRationale(this)) {
        // En caso de que se denieguen los permisos con la marca de "No volver a preguntar"
        DemoUtils.launchPermissionSettings(this);
      } else {
        Toast.makeText(
                this, "Los permisos de la camara son necesarios para ejecutar la aplicacion", Toast.LENGTH_LONG)
            .show();
      }
      finish();
    }
  }

  @Override
  public void onWindowFocusChanged(boolean hasFocus) {
    super.onWindowFocusChanged(hasFocus);
    if (hasFocus) {
      getWindow()
          .getDecorView()
          .setSystemUiVisibility(
              View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                  | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                  | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                  | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                  | View.SYSTEM_UI_FLAG_FULLSCREEN
                  | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY);
      getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
    }
  }

  private void onSingleTap(MotionEvent tap) {
    if (!hasFinishedLoading) {
      // No hacemos nada si se da un toque y no ha terminado de cargar
      return;
    }

    Frame frame = arSceneView.getArFrame();
    if (frame != null) {
      if (!hasPlacedSolarSystem && tryPlaceSolarSystem(tap, frame)) {
        hasPlacedSolarSystem = true;
      }
    }
  }

  private boolean tryPlaceSolarSystem(MotionEvent tap, Frame frame) {
    if (tap != null && frame.getCamera().getTrackingState() == TrackingState.TRACKING) {
      for (HitResult hit : frame.hitTest(tap)) {
        Trackable trackable = hit.getTrackable();
        if (trackable instanceof Plane && ((Plane) trackable).isPoseInPolygon(hit.getHitPose())) {
          // Creamos un ancla donde se da el toque para conectar el sistema solar
          Anchor anchor = hit.createAnchor();
          AnchorNode anchorNode = new AnchorNode(anchor);
          anchorNode.setParent(arSceneView.getScene());

          // Creamos el sistema solar 
          Node solarSystem = createSolarSystem();

          // Anclar el sistema solar al ancla
          anchorNode.addChild(solarSystem);
          return true;
        }
      }
    }

    return false;
  }

  // Metodo para crear el sistema solar
  private Node createSolarSystem() {
    // Creamos la base del sistema solar
    Node base = new Node();
    
    // Creamos el sol
    Node sun = new Node();
    sun.setParent(base);

    // Colocamos el sol
    sun.setLocalPosition(new Vector3(0.0f, 0.5f, 0.0f));

    // Creamos el modelo renderizado del sol
    Node sunVisual = new Node();
    sunVisual.setParent(sun);

    // Establecemos el modelo renderizado
    sunVisual.setRenderable(sunRenderable);

    // Establecemos la escala del modelo
    sunVisual.setLocalScale(new Vector3(0.5f, 0.5f, 0.5f));

    // Creamos los controles del sistema solar
    Node solarControls = new Node();
    solarControls.setParent(sun);

    // Establecemos el modelo renderizado
    solarControls.setRenderable(solarControlsRenderable);

    // Colocamos los controles del sol
    solarControls.setLocalPosition(new Vector3(0.0f, 0.25f, 0.0f));

    // Establecemos la vista del controlador
    View solarControlsView = solarControlsRenderable.getView();

    // Establecemos los controladores de velocidad de orbita
    SeekBar orbitSpeedBar = solarControlsView.findViewById(R.id.orbitSpeedBar);
    orbitSpeedBar.setProgress((int) (solarSettings.getOrbitSpeedMultiplier() * 10.0f));
    orbitSpeedBar.setOnSeekBarChangeListener(
        new SeekBar.OnSeekBarChangeListener() {
          @Override
          public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
            float ratio = (float) progress / (float) orbitSpeedBar.getMax();
            solarSettings.setOrbitSpeedMultiplier(ratio * 10.0f);
          }

          @Override
          public void onStartTrackingTouch(SeekBar seekBar) {}

          @Override
          public void onStopTrackingTouch(SeekBar seekBar) {}
        });

    // Establecemos los controladores de rotacion de orbita
    SeekBar rotationSpeedBar = solarControlsView.findViewById(R.id.rotationSpeedBar);
    rotationSpeedBar.setProgress((int) (solarSettings.getRotationSpeedMultiplier() * 10.0f));
    rotationSpeedBar.setOnSeekBarChangeListener(
        new SeekBar.OnSeekBarChangeListener() {
          @Override
          public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
            float ratio = (float) progress / (float) rotationSpeedBar.getMax();
            solarSettings.setRotationSpeedMultiplier(ratio * 10.0f);
          }

          @Override
          public void onStartTrackingTouch(SeekBar seekBar) {}

          @Override
          public void onStopTrackingTouch(SeekBar seekBar) {}
        });

    // Activamos los controles del sistema solar cuando damos un toque en el sol
    sunVisual.setOnTapListener(
        (hitTestResult, motionEvent) -> solarControls.setEnabled(!solarControls.isEnabled()));

    // Creamos los planetas con los atributos deseados, aquellos planetas que tengan satelites
    // deben crearse como variables para definirlas como los padres de los satelites
    createPlanet("Mercury", sun, 0.4f, 47f, mercuryRenderable, 0.019f, 0.03f);

    createPlanet("Venus", sun, 0.7f, 35f, venusRenderable, 0.0475f, 2.64f);

    Node earth = createPlanet("Earth", sun, 1.0f, 29f, earthRenderable, 0.05f, 23.4f);

    createPlanet("Moon", earth, 0.15f, 100f, lunaRenderable, 0.018f, 6.68f);

    createPlanet("Mars", sun, 1.5f, 24f, marsRenderable, 0.0265f, 25.19f);

    createPlanet("Jupiter", sun, 2.2f, 13f, jupiterRenderable, 0.16f, 3.13f);

    createPlanet("Saturn", sun, 3.5f, 9f, saturnRenderable, 0.1325f, 26.73f);

    createPlanet("Uranus", sun, 5.2f, 7f, uranusRenderable, 0.1f, 82.23f);

    createPlanet("Neptune", sun, 6.1f, 5f, neptuneRenderable, 0.074f, 28.32f);

    return base;
  }

  // Metodo para crear los planetas
  private Node createPlanet(
      String name,
      Node parent,
      float auFromParent,
      float orbitDegreesPerSecond,
      ModelRenderable renderable,
      float planetScale,
      float axisTilt) {

    // La orbita es de tipo RotatingNode debido a que se busca que cada planeta rote con su propia velocidad

    RotatingNode orbit = new RotatingNode(solarSettings, true, false, 0);
    orbit.setDegreesPerSecond(orbitDegreesPerSecond);
    orbit.setParent(parent);

    // Creamos el planeta y su posición relativa con el Sol 

    Planet planet =
        new Planet(
            this, name, planetScale, orbitDegreesPerSecond, axisTilt, renderable, solarSettings);
    planet.setParent(orbit);
    planet.setLocalPosition(new Vector3(auFromParent * AU_TO_METERS, 0.0f, 0.0f));

    return planet;
  }

  // Metodo para mostrar el mensaje de carga
  private void showLoadingMessage() {
    if (loadingMessageSnackbar != null && loadingMessageSnackbar.isShownOrQueued()) {
      return;
    }

    loadingMessageSnackbar =
        Snackbar.make(
            SolarActivity.this.findViewById(android.R.id.content),
            R.string.plane_finding,
            Snackbar.LENGTH_INDEFINITE);
    loadingMessageSnackbar.getView().setBackgroundColor(0xbf323232);
    loadingMessageSnackbar.show();
  }

  // Metodo para ocultar el mensaje de carga
  private void hideLoadingMessage() {
    if (loadingMessageSnackbar == null) {
      return;
    }

    loadingMessageSnackbar.dismiss();
    loadingMessageSnackbar = null;
  }
}
