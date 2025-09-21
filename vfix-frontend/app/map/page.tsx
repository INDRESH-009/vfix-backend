"use client";

import dynamic from "next/dynamic";
import { useEffect, useMemo, useState } from "react";

const Map = dynamic(() => import("./parts/MapClient"), { ssr: false });

export default function MapPage() {
  const [center, setCenter] = useState<[number, number]>([12.9716, 77.5946]);

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(p => {
        setCenter([p.coords.latitude, p.coords.longitude]);
      });
    }
  }, []);

  return (
    <div className="card p-0 overflow-hidden">
      <Map center={center} />
    </div>
  );
}
