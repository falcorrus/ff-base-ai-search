"use client";
import React, { useState, useEffect, useMemo } from "react";
import type { Container, Engine } from "@tsparticles/engine";
import Particles, { initParticlesEngine } from "@tsparticles/react";
import { loadSlim } from "@tsparticles/slim";
import type { ISourceOptions } from "@tsparticles/engine";

interface SparklesCoreProps {
  id?: string;
  className?: string;
  background?: string;
  minSize?: number;
  maxSize?: number;
  speed?: number;
  particleColor?: string;
  particleDensity?: number;
}

export const SparklesCore = (props: SparklesCoreProps) => {
  const {
    id,
    className,
    background,
    minSize,
    maxSize,
    speed,
    particleColor,
    particleDensity,
  } = props;

  const [init, setInit] = useState(false);

  useEffect(() => {
    initParticlesEngine(async (engine) => {
      await loadSlim(engine);
    }).then(() => {
      setInit(true);
    });
  }, []);

  const options: ISourceOptions = useMemo(() => {
    return {
      background: {
        color: {
          value: background || "#000000",
        },
      },
      fpsLimit: 120,
      particles: {
        number: {
          value: particleDensity || 120,
          density: {
            enable: true,
            value_area: 800,
          },
        },
        color: {
          value: particleColor || "#ffffff",
        },
        shape: {
          type: "circle",
        },
        opacity: {
          value: { min: 0.1, max: 1 },
          random: true,
          anim: {
            enable: true,
            speed: speed || 1,
            opacity_min: 0.1,
            sync: false,
          },
        },
        size: {
          value: { min: minSize || 1, max: maxSize || 3 },
          random: true,
          anim: {
            enable: true,
            speed: speed || 1,
            size_min: minSize || 1,
            sync: false,
          },
        },
        line_linked: {
          enable: false,
        },
        move: {
          enable: true,
          speed: speed || 1,
          direction: "none",
          random: true,
          straight: false,
          out_mode: "out",
          bounce: false,
          attract: {
            enable: false,
            rotateX: 600,
            rotateY: 1200,
          },
        },
      },
      detectRetina: true,
    };
  }, [minSize, maxSize, speed, particleColor, particleDensity, background]);

  return (
    <div className={className} id={id}>
      {init && (
        <Particles
          id={id || "tsparticles"}
          options={options}
        />
      )}
    </div>
  );
};