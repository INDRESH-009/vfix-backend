"use client";

import { useEffect, useState } from "react";
import { apiPOST } from "@/lib/api";
import toast from "react-hot-toast";

type IssueOut = {
  id: string; status: string; lat: number; lng: number; media: {url:string}[];
};

export default function ReportPage() {
  const [desc, setDesc] = useState("");
  const [category, setCategory] = useState("Sanitation");
  const [lat, setLat] = useState<number | null>(null);
  const [lng, setLng] = useState<number | null>(null);
  const [address, setAddress] = useState("");
  const [files, setFiles] = useState<FileList | null>(null);

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((pos) => {
        setLat(pos.coords.latitude);
        setLng(pos.coords.longitude);
      }, () => toast("Location permission denied"));
    }
  }, []);

  async function submit() {
    if (!lat || !lng) { toast.error("Location not available"); return; }
    const payload = {
      description: desc,
      category,
      lat, lng,
      address,
      public_visibility: true,
      consent: true
    };
    const fd = new FormData();
    fd.append("json_str", JSON.stringify(payload));
    if (files) {
      // backend accepts both `photos` and `photos[]`
      Array.from(files).forEach(f => fd.append("photos", f));
    }

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/issues`, {
        method: "POST",
        headers: { Authorization: `Bearer ${localStorage.getItem("jwt")}` || "" },
        body: fd,
      });
      if (!res.ok) throw new Error(await res.text());
      const data: IssueOut = await res.json();
      toast.success("Issue submitted");
      window.location.href = `/issues/${data.id}`;
    } catch (e: any) {
      toast.error(e.message || "Failed to submit");
    }
  }

  return (
    <div className="max-w-2xl mx-auto card">
      <h1 className="text-xl font-semibold mb-4">Report an Issue</h1>

      <label className="label">Category</label>
      <select className="input mb-3" value={category} onChange={e=>setCategory(e.target.value)}>
        <option>Sanitation</option>
        <option>Roads</option>
        <option>Water</option>
        <option>Electricity</option>
      </select>

      <label className="label">Description</label>
      <textarea className="input mb-3" rows={4} value={desc} onChange={e=>setDesc(e.target.value)} />

      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="label">Latitude</label>
          <input className="input" value={lat ?? ""} onChange={e=>setLat(parseFloat(e.target.value))} />
        </div>
        <div>
          <label className="label">Longitude</label>
          <input className="input" value={lng ?? ""} onChange={e=>setLng(parseFloat(e.target.value))} />
        </div>
      </div>

      <label className="label mt-3">Address (optional)</label>
      <input className="input mb-3" value={address} onChange={e=>setAddress(e.target.value)} />

      <label className="label">Photos</label>
      <input className="input mb-4" type="file" multiple onChange={e=>setFiles(e.target.files)} />

      <button className="btn btn-primary" onClick={submit}>Submit</button>
    </div>
  );
}
