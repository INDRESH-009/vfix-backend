"use client";

import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { useEffect, useState } from "react";

type PublicIssue = {
  id: string; category?: string; status: string; severity?: number | null;
  lat: number; lng: number; created_at: string; thumb?: string | null;
};

function BBoxFetcher({ onData }: { onData: (items: PublicIssue[]) => void }) {
  const map = useMapEvents({
    moveend: async () => {
      const b = map.getBounds();
      const bbox = `${b.getWest()},${b.getSouth()},${b.getEast()},${b.getNorth()}`;
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/public/issues?bbox=${bbox}`);
      const data = await res.json();
      onData(data.items || []);
    }
  });

  useEffect(() => {
    // initial fetch
    const b = map.getBounds();
    const bbox = `${b.getWest()},${b.getSouth()},${b.getEast()},${b.getNorth()}`;
    fetch(`${process.env.NEXT_PUBLIC_API_BASE}/public/issues?bbox=${bbox}`)
      .then(r=>r.json()).then(d=>onData(d.items || []));
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return null;
}

export default function MapClient({ center }: { center: [number, number] }) {
  const [items, setItems] = useState<PublicIssue[]>([]);

  return (
    <MapContainer center={center} zoom={14} style={{ height: "70vh", width: "100%" }}>
      <TileLayer
        attribution='&copy; OpenStreetMap'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <BBoxFetcher onData={setItems} />
      {items.map((i) => (
        <Marker position={[i.lat, i.lng]} key={i.id}>
          <Popup>
            <div className="text-sm">
              <div><b>{i.category || "Issue"}</b> — {i.status} {i.severity != null && `(sev ${i.severity})`}</div>
              <div>{new Date(i.created_at).toLocaleString()}</div>
              {i.thumb && (
                // eslint-disable-next-line @next/next/no-img-element
                <img src={i.thumb} alt="" className="mt-2 w-40 h-24 object-cover rounded-md border"/>
              )}
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}
