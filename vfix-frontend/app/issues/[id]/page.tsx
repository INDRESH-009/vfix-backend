"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { apiGET } from "@/lib/api";

type Media = { id: string; role: string; url: string };
type Issue = {
  id: string; status: string; category?: string; severity?: number | null;
  description: string; address?: string; lat: number; lng: number;
  created_at: string; sla_due_at?: string | null; media: Media[];
};

export default function IssueDetailPage() {
  const params = useParams<{ id: string }>();
  const [issue, setIssue] = useState<Issue | null>(null);

  useEffect(() => {
    apiGET<Issue>(`/issues/${params.id}`).then(setIssue).catch(()=>setIssue(null));
  }, [params.id]);

  if (!issue) return <div>Loading…</div>;

  return (
    <div className="grid gap-4 md:grid-cols-3">
      <div className="card md:col-span-2">
        <h1 className="text-xl font-semibold mb-2">Issue #{issue.id.slice(0,8)}</h1>
        <div className="flex gap-2 mb-2">
          <span className="badge">{issue.category || "Uncategorized"}</span>
          <span className="badge">{issue.status}</span>
          {issue.severity != null && <span className="badge">sev {issue.severity}</span>}
        </div>
        <div className="text-sm text-gray-600 mb-2">
          Created: {new Date(issue.created_at).toLocaleString()} {issue.sla_due_at && `• SLA: ${new Date(issue.sla_due_at).toLocaleString()}`}
        </div>
        <p className="mb-3 whitespace-pre-wrap">{issue.description}</p>
        {issue.address && <p className="text-sm">📍 {issue.address}</p>}

        <div className="grid grid-cols-2 gap-2 mt-4">
          {issue.media.map(m => (
            // eslint-disable-next-line @next/next/no-img-element
            <img key={m.id} src={m.url} className="w-full h-44 object-cover rounded-md border" alt="" />
          ))}
        </div>
      </div>

      <div className="card">
        <h3 className="font-semibold mb-2">Location</h3>
        <div className="text-sm">Lat: {issue.lat.toFixed(5)}<br/>Lng: {issue.lng.toFixed(5)}</div>
        <a
          className="btn mt-3"
          href={`https://www.google.com/maps?q=${issue.lat},${issue.lng}`}
          target="_blank"
        >Open in Google Maps</a>
      </div>
    </div>
  );
}
