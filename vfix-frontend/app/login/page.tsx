"use client";

import { useState } from "react";
import { apiPOST, setToken } from "@/lib/api";
import toast from "react-hot-toast";

export default function LoginPage() {
  const [identifier, setIdentifier] = useState("+911234567890");
  const [code, setCode] = useState("");

  async function start() {
    try {
      await apiPOST("/auth/otp/start", { identifier });
      toast.success("OTP sent (dev: 123456)");
    } catch (e: any) {
      toast.error(e.message || "Failed");
    }
  }

  async function verify() {
    try {
      const data = await apiPOST<{access_token: string}>("/auth/otp/verify", { identifier, code });
      setToken(data.access_token);
      toast.success("Logged in");
      window.location.href = "/issues";
    } catch (e: any) {
      toast.error(e.message || "Invalid code");
    }
  }

  return (
    <div className="max-w-md mx-auto card">
      <h1 className="text-xl font-semibold mb-4">Login</h1>
      <label className="label">Phone or Email</label>
      <input className="input mb-3" value={identifier} onChange={(e)=>setIdentifier(e.target.value)} />

      <div className="flex gap-2 mb-4">
        <button className="btn btn-primary" onClick={start}>Send OTP</button>
        <button className="btn" onClick={()=>{ setCode("123456"); }}>Use dev code</button>
      </div>

      <label className="label">Enter Code</label>
      <input className="input mb-3" value={code} onChange={(e)=>setCode(e.target.value)} />
      <button className="btn btn-primary" onClick={verify}>Verify & Continue</button>
    </div>
  );
}
