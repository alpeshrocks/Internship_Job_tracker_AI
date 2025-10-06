import React, { useEffect, useState } from "react";
import { Container, TextField, Select, MenuItem, Button, Card, CardContent, Chip, Checkbox, FormControlLabel, Stack, Pagination } from "@mui/material";
const API = import.meta.env.VITE_API_BASE || "http://localhost:8000";

async function fetchJobs({ q="", applied=null, page=1, pageSize=20 }){
  const params = new URLSearchParams();
  if (q) params.set("q", q);
  if (applied !== null) params.set("applied", applied);
  params.set("limit", pageSize);
  params.set("offset", (page-1)*pageSize);
  const res = await fetch(`${API}/jobs?`+params.toString());
  return res.json();
}
async function patchApplication(id, payload){
  const res = await fetch(`${API}/jobs/${id}/application`, { method:"PATCH", headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)});
  return res.json();
}

export default function App(){
  const [q,setQ]=useState("");
  const [applied,setApplied]=useState(null);
  const [jobs,setJobs]=useState([]);
  const [page,setPage]=useState(1);

  const load = async ()=>{
    const data = await fetchJobs({ q, applied, page });
    setJobs(data);
  };
  useEffect(()=>{ load(); }, [q, applied, page]);

  const onToggleApplied = async (job)=>{
    await patchApplication(job.id, { applied: !job.applied });
    load();
  };

  return (
    <Container maxWidth="md" sx={{ py: 3 }}>
      <h1>Internship Tracker Pro</h1>
      <Stack direction="row" spacing={2} sx={{ mb: 2 }}>
        <TextField label="Search" fullWidth value={q} onChange={e=>setQ(e.target.value)} onKeyDown={e=> e.key==='Enter' && load() }/>
        <Select value={applied===null?'all': applied? 'true':'false'} onChange={e=>{
          const v = e.target.value;
          setApplied(v==='all'? null : v==='true'); setPage(1);
        }}>
          <MenuItem value="all">All</MenuItem>
          <MenuItem value="false">Not Applied</MenuItem>
          <MenuItem value="true">Applied</MenuItem>
        </Select>
        <Button variant="contained" onClick={load}>Refresh</Button>
      </Stack>

      <Stack spacing={2}>
        {jobs.map(j=>(
          <Card key={j.id}>
            <CardContent>
              <div style={{fontWeight:700}}><a href={j.link} target="_blank" rel="noreferrer">{j.title}</a></div>
              <div>{j.company} · {j.location || ""}</div>
              <Stack direction="row" spacing={1} sx={{ my: 1, flexWrap:'wrap' }}>
                <Chip label={j.source} variant="outlined"/>
                {j.remote_ok && <Chip label="Remote" variant="outlined"/>}
                {(j.skills||[]).slice(0,6).map(s=> <Chip key={s} size="small" label={s}/>)}
              </Stack>
              <FormControlLabel control={<Checkbox checked={j.applied} onChange={()=>onToggleApplied(j)} />} label="Applied"/>
              <TextField fullWidth defaultValue={j.notes||""} placeholder="Notes..." onBlur={async e=>{ await patchApplication(j.id, { notes:e.target.value }); }}/>
            </CardContent>
          </Card>
        ))}
      </Stack>

      <Stack alignItems="center" sx={{ mt: 2 }}>
        <Pagination count={5} page={page} onChange={(_,p)=>setPage(p)} />
      </Stack>
    </Container>
  );
}
