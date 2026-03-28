import { useEffect, useRef } from "react";
import {
  Cartesian2,
  Cartesian3,
  ClockRange,
  ClockStep,
  Color,
  CustomDataSource,
  Entity,
  HorizontalOrigin,
  JulianDate,
  LabelStyle,
  PolylineGlowMaterialProperty,
  SampledPositionProperty,
  ScreenSpaceEventType,
  VerticalOrigin,
  Viewer,
} from "cesium";

import type { DeepSpaceObject, Mode, NeoObject, OrbitObject, SolarBody } from "@/types/api";


const AU_SCALE_METERS = 12_000_000;
const LIGHT_YEAR_SCALE_METERS = 40_000;


function orbitPointToCartesian(point: { latitude: number; longitude: number; altitude_km: number }) {
  return Cartesian3.fromDegrees(point.longitude, point.latitude, point.altitude_km * 1000);
}

function vectorToCartesian(vector: { x: number; y: number; z: number }, scale: number) {
  return new Cartesian3(vector.x * scale, vector.y * scale, vector.z * scale);
}

function entityScale(radiusKm: number, minimum: number) {
  return Math.max(minimum, Math.cbrt(Math.max(radiusKm, 1)) * minimum * 0.4);
}


interface CesiumViewportProps {
  sceneMode: Exclude<Mode, "featured-tours">;
  selectedId: string | null;
  followSelection: boolean;
  playing: boolean;
  speed: number;
  orbitObjects: OrbitObject[];
  solarBodies: SolarBody[];
  neoObjects: NeoObject[];
  deepSpaceObjects: DeepSpaceObject[];
  onSelectObject: (id: string) => void;
}


export function CesiumViewport({
  sceneMode,
  selectedId,
  followSelection,
  playing,
  speed,
  orbitObjects,
  solarBodies,
  neoObjects,
  deepSpaceObjects,
  onSelectObject,
}: CesiumViewportProps) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const viewerRef = useRef<Viewer | null>(null);
  const orbitSourceRef = useRef<CustomDataSource | null>(null);
  const solarSourceRef = useRef<CustomDataSource | null>(null);
  const neoSourceRef = useRef<CustomDataSource | null>(null);
  const deepSourceRef = useRef<CustomDataSource | null>(null);
  const latestSelectRef = useRef(onSelectObject);
  const previousModeRef = useRef<Mode | null>(null);

  latestSelectRef.current = onSelectObject;

  useEffect(() => {
    if (!containerRef.current || viewerRef.current) {
      return;
    }

    const viewer = new Viewer(containerRef.current, {
      animation: false,
      timeline: false,
      baseLayerPicker: false,
      geocoder: false,
      homeButton: false,
      infoBox: false,
      sceneModePicker: false,
      selectionIndicator: false,
      navigationHelpButton: false,
      fullscreenButton: false,
      shouldAnimate: true,
    });

    viewer.scene.postProcessStages.fxaa.enabled = true;
    viewer.scene.globe.enableLighting = true;
    viewer.scene.globe.baseColor = Color.fromCssColorString("#07101b");
    viewer.scene.backgroundColor = Color.fromCssColorString("#020610");
    viewer.clock.clockRange = ClockRange.LOOP_STOP;
    viewer.clock.clockStep = ClockStep.SYSTEM_CLOCK_MULTIPLIER;

    const orbitSource = new CustomDataSource("orbit");
    const solarSource = new CustomDataSource("solar");
    const neoSource = new CustomDataSource("neo");
    const deepSource = new CustomDataSource("deep-space");

    viewer.dataSources.add(orbitSource);
    viewer.dataSources.add(solarSource);
    viewer.dataSources.add(neoSource);
    viewer.dataSources.add(deepSource);

    viewer.screenSpaceEventHandler.setInputAction((movement: { position: Cartesian2 }) => {
      const picked = viewer.scene.pick(movement.position);
      const entity = picked?.id as Entity | undefined;
      if (entity && typeof entity.id === "string") {
        latestSelectRef.current(entity.id);
      }
    }, ScreenSpaceEventType.LEFT_CLICK);

    viewerRef.current = viewer;
    orbitSourceRef.current = orbitSource;
    solarSourceRef.current = solarSource;
    neoSourceRef.current = neoSource;
    deepSourceRef.current = deepSource;

    return () => {
      viewer.destroy();
      viewerRef.current = null;
      orbitSourceRef.current = null;
      solarSourceRef.current = null;
      neoSourceRef.current = null;
      deepSourceRef.current = null;
    };
  }, []);

  useEffect(() => {
    const viewer = viewerRef.current;
    const orbitSource = orbitSourceRef.current;
    const solarSource = solarSourceRef.current;
    const neoSource = neoSourceRef.current;
    const deepSource = deepSourceRef.current;

    if (!viewer || !orbitSource || !solarSource || !neoSource || !deepSource) {
      return;
    }

    orbitSource.show = sceneMode === "earth-orbit";
    solarSource.show = sceneMode === "solar-system";
    neoSource.show = sceneMode === "neo";
    deepSource.show = sceneMode === "deep-space";

    orbitSource.entities.removeAll();
    solarSource.entities.removeAll();
    neoSource.entities.removeAll();
    deepSource.entities.removeAll();

    if (sceneMode === "earth-orbit") {
      viewer.scene.globe.show = true;
      if (viewer.scene.skyAtmosphere) {
        viewer.scene.skyAtmosphere.show = true;
      }
      if (viewer.scene.moon) {
        viewer.scene.moon.show = true;
      }

      orbitObjects.forEach((item) => {
        const track = item.ground_track.length ? item.ground_track : item.trail;
        const property = new SampledPositionProperty();
        track.forEach((point) => {
          property.addSample(JulianDate.fromIso8601(point.timestamp), orbitPointToCartesian(point));
        });
        orbitSource.entities.add({
          id: item.id,
          name: item.name,
          position: property,
          point: {
            pixelSize: item.tracked ? 12 : 7,
            color: Color.fromCssColorString(item.tracked ? "#ffca6b" : "#79d2ff"),
            outlineColor: Color.fromCssColorString("#061018"),
            outlineWidth: 2,
          },
          label: {
            text: item.name,
            font: item.tracked ? "600 14px 'IBM Plex Sans'" : "500 12px 'IBM Plex Sans'",
            fillColor: Color.WHITE,
            outlineColor: Color.fromCssColorString("#061018"),
            outlineWidth: 3,
            style: LabelStyle.FILL_AND_OUTLINE,
            pixelOffset: new Cartesian2(0, -18),
            show: item.tracked || item.id === selectedId,
          },
          polyline: {
            positions: track.map(orbitPointToCartesian),
            width: item.tracked ? 2.5 : 1.4,
            material: new PolylineGlowMaterialProperty({
              color: Color.fromCssColorString(item.tracked ? "#ffd78a" : "#51b5e0").withAlpha(0.72),
              glowPower: item.tracked ? 0.24 : 0.12,
            }),
          },
        });
      });

      const sampleTrack = orbitObjects[0]?.ground_track;
      if (sampleTrack?.length) {
        viewer.clock.startTime = JulianDate.fromIso8601(sampleTrack[0].timestamp);
        viewer.clock.stopTime = JulianDate.fromIso8601(sampleTrack[sampleTrack.length - 1].timestamp);
        viewer.clock.currentTime = JulianDate.fromIso8601(sampleTrack[0].timestamp);
      }
    }

    if (sceneMode === "solar-system") {
      viewer.scene.globe.show = false;
      if (viewer.scene.skyAtmosphere) {
        viewer.scene.skyAtmosphere.show = false;
      }
      if (viewer.scene.moon) {
        viewer.scene.moon.show = false;
      }

      solarBodies.forEach((body) => {
        const position = vectorToCartesian(body.position_au, AU_SCALE_METERS);
        const scale = entityScale(body.radius_km, body.kind === "star" ? 320_000 : 90_000);
        if (body.orbit_path_au.length) {
          solarSource.entities.add({
            id: `${body.id}-orbit`,
            polyline: {
              positions: body.orbit_path_au.map((point) => vectorToCartesian(point, AU_SCALE_METERS)),
              width: 1.2,
              material: Color.fromCssColorString("#2a5b8f").withAlpha(0.55),
            },
          });
        }
        solarSource.entities.add({
          id: body.id,
          name: body.name,
          position,
          ellipsoid: {
            radii: new Cartesian3(scale, scale, scale),
            material: Color.fromCssColorString(body.color).withAlpha(body.kind === "star" ? 0.96 : 0.86),
          },
          label: {
            text: body.name,
            font: "600 13px 'IBM Plex Sans'",
            fillColor: Color.WHITE,
            style: LabelStyle.FILL_AND_OUTLINE,
            outlineWidth: 3,
            pixelOffset: new Cartesian2(0, -20),
            show: body.kind !== "moon" || body.id === selectedId,
          },
        });
      });
    }

    if (sceneMode === "neo") {
      viewer.scene.globe.show = false;
      if (viewer.scene.skyAtmosphere) {
        viewer.scene.skyAtmosphere.show = false;
      }
      if (viewer.scene.moon) {
        viewer.scene.moon.show = false;
      }

      neoSource.entities.add({
        id: "neo-earth-reference",
        position: vectorToCartesian({ x: 1, y: 0, z: 0 }, AU_SCALE_METERS),
        ellipsoid: {
          radii: new Cartesian3(120_000, 120_000, 120_000),
          material: Color.fromCssColorString("#5aa3ff").withAlpha(0.9),
        },
        label: {
          text: "Earth",
          fillColor: Color.WHITE,
          style: LabelStyle.FILL_AND_OUTLINE,
          outlineWidth: 2,
          pixelOffset: new Cartesian2(0, -18),
        },
      });
      neoSource.entities.add({
        id: "neo-sun-reference",
        position: Cartesian3.ZERO,
        ellipsoid: {
          radii: new Cartesian3(220_000, 220_000, 220_000),
          material: Color.fromCssColorString("#f7b233").withAlpha(0.95),
        },
      });

      neoObjects.forEach((item) => {
        if (!item.position_au) {
          return;
        }
        const selected = item.id === selectedId;
        neoSource.entities.add({
          id: item.id,
          name: item.name,
          position: vectorToCartesian(item.position_au, AU_SCALE_METERS),
          point: {
            pixelSize: selected ? 14 : 10,
            color: Color.fromCssColorString(item.is_hazardous ? "#ff7f68" : "#a5d8a2"),
            outlineColor: Color.fromCssColorString("#08111a"),
            outlineWidth: 2,
          },
          label: {
            text: item.name,
            font: "600 12px 'IBM Plex Sans'",
            fillColor: Color.WHITE,
            style: LabelStyle.FILL_AND_OUTLINE,
            outlineWidth: 2,
            pixelOffset: new Cartesian2(0, -18),
            show: selected || item.is_hazardous,
          },
        });
      });
    }

    if (sceneMode === "deep-space") {
      viewer.scene.globe.show = false;
      if (viewer.scene.skyAtmosphere) {
        viewer.scene.skyAtmosphere.show = false;
      }
      if (viewer.scene.moon) {
        viewer.scene.moon.show = false;
      }

      deepSpaceObjects.forEach((item) => {
        const position = vectorToCartesian(item.galactic_position ?? { x: 0, y: 0, z: 0 }, LIGHT_YEAR_SCALE_METERS);
        const selected = item.id === selectedId;
        const color =
          item.category === "compact-object"
            ? "#e6b777"
            : item.category === "nebula"
              ? "#7bc3ff"
              : item.category === "galactic-context"
                ? "#4d73b9"
                : "#c8d6ff";

        deepSource.entities.add({
          id: item.id,
          name: item.name,
          position,
          point: {
            pixelSize: selected ? 12 : 8,
            color: Color.fromCssColorString(color),
            outlineColor: Color.fromCssColorString("#040912"),
            outlineWidth: 2,
          },
          label: {
            text: item.name,
            font: "600 12px 'IBM Plex Sans'",
            fillColor: Color.WHITE,
            style: LabelStyle.FILL_AND_OUTLINE,
            outlineWidth: 2,
            pixelOffset: new Cartesian2(0, -16),
            show: selected || item.category !== "galactic-context",
          },
        });
      });
    }

    viewer.clock.shouldAnimate = playing;
    viewer.clock.multiplier = speed;

    const activeSource =
      sceneMode === "earth-orbit"
        ? orbitSource
        : sceneMode === "solar-system"
          ? solarSource
          : sceneMode === "neo"
            ? neoSource
            : deepSource;

    if (followSelection && selectedId) {
      const target = activeSource.entities.getById(selectedId);
      viewer.trackedEntity = target ?? undefined;
    } else {
      viewer.trackedEntity = undefined;
    }

    if (previousModeRef.current !== sceneMode) {
      previousModeRef.current = sceneMode;
      const destination =
        sceneMode === "earth-orbit"
          ? Cartesian3.fromDegrees(-35, 18, 22_000_000)
          : sceneMode === "solar-system"
            ? new Cartesian3(0, 85_000_000, 62_000_000)
            : sceneMode === "neo"
              ? new Cartesian3(0, 32_000_000, 18_000_000)
              : new Cartesian3(0, 7_000_000, 5_000_000);
      viewer.camera.flyTo({ destination, duration: 1.6 });
    }
  }, [deepSpaceObjects, followSelection, neoObjects, orbitObjects, playing, sceneMode, selectedId, solarBodies, speed]);

  return <div ref={containerRef} className="cesium-viewport" />;
}
