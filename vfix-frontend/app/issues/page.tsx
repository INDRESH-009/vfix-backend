"use client";

import { useEffect, useState } from "react";
import { apiGET } from "@/lib/api";
import Link from "next/link";

type Media = { id: string; role: string; url: string };
type Issue = {
  id: string; status: string; category?: string; severity?: number | null;
  created_at: string; media: Media[]; address?: string;
};

export default function MyIssuesPage() {
  const [items, setItems] = useState<Issue[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiGET<{items: Issue[]}>("/issues/mine")
      .then(res => setItems(res.items))
      .catch(() => setItems([]))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading…</div>;

  return (
    <div>
      <h1 className="text-xl font-semibold mb-4">My Issues</h1>
      <div className="grid gap-3">
        {items.map(i => (
          <Link href={`/issues/${i.id}`} key={i.id} className="card block">
            <div className="flex gap-3">
              {i.media?.[0]?.url && (
                // eslint-disable-next-line @next/next/no-img-element
                <img src={i.media[0].url} alt="" className="w-24 h-24 object-cover rounded-md border" />
              )}
              <div>
                <div className="flex gap-2 items-center">
                  <span className="badge">{i.category || "Uncategorized"}</span>
                  <span className="badge">{i.status}</span>
                  {i.severity != null && <span className="badge">sev {i.severity}</span>}
                </div>
                <div className="text-sm text-gray-600 mt-1">{new Date(i.created_at).toLocaleString()}</div>
                {i.address && <div className="text-sm mt-1">{i.address}</div>}
              </div>
            </div>
          </Link>
        ))}
        {items.length === 0 && <div className="card">No issues yet. <a href="/report" className="text-blue-600">Report one</a>.</div>}
      </div>
    </div>
  );
}
