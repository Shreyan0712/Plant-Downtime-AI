import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import { WorkspaceView, InfoBox, ChatResponse } from './models';

const API = 'http://127.0.0.1:8000';   // your FastAPI base URL

@Injectable({ providedIn: 'root' })
export class WorkspaceService {

  constructor(private http: HttpClient) {}

  // --- generic GET helper -------------------------------------------------
  private async get(path: string): Promise<any[]> {
    try {
      const data = await firstValueFrom(this.http.get<any[]>(`${API}${path}`));
      return Array.isArray(data) ? data : [];
    } catch {
      return [];
    }
  }

  // --- column derivation --------------------------------------------------
  private columnsOf(rows: any[]): string[] {
    return rows.length ? Object.keys(rows[0]) : [];
  }

  // --- VIEW BUILDERS (mirror your build_* functions) ----------------------

  async buildMachines(): Promise<WorkspaceView> {
    const rows = await this.get('/machines');
    const running = rows.filter(r => String(r.status).toLowerCase() === 'running').length;
    const notRunning = rows.length - running;
    const categories = new Set(rows.map(r => r.category)).size;
    const boxes: InfoBox[] = [
      { title: 'Total Machines', stat: String(rows.length), body: `${running} running · ${notRunning} not running` },
      { title: 'Running', stat: String(running), body: 'Currently operational' },
      { title: 'Not Running', stat: String(notRunning), body: 'Idle / down / maintenance' },
      { title: 'Categories', stat: String(categories), body: 'Distinct machine types' },
    ];
    const charts = [
      this.countsChart('Machines by Status', rows.map(r => r.status), 'donut'),
      this.countsChart('Machines by Category', rows.map(r => r.category), 'bar'),
    ];

    return { title: 'Machines', rows, columns: this.columnsOf(rows), infoBoxes: boxes, charts };
  }

  async buildMaintenance(): Promise<WorkspaceView> {
    const rows = await this.get('/maintenance-logs');
    const techs = new Set(rows.map(r => r.technician)).size;
    const machines = new Set(rows.map(r => r.machine_id)).size;
    const types = rows.map(r => r.maintenance_type);
    const topType = types.length ? this.mode(types) : '-';
    const boxes: InfoBox[] = [
      { title: 'Total Logs', stat: String(rows.length), body: 'Maintenance records' },
      { title: 'Most Common', stat: topType, body: 'Maintenance type' },
      { title: 'Technicians', stat: String(techs), body: 'Distinct technicians' },
      { title: 'Machines Covered', stat: String(machines), body: 'Serviced machines' },
    ];
    const charts = [
      this.countsChart('Logs by Type', rows.map(r => r.maintenance_type), 'donut'),
      this.topCountsChart('Logs by Technician (top 10)', rows.map(r => r.technician), 10, 'bar'),
    ];
    return { title: 'Maintenance Logs', rows, columns: this.columnsOf(rows), infoBoxes: boxes, charts };
  }

  async buildDowntime(): Promise<WorkspaceView> {
    const rows = await this.get('/downtime-events');
    const totalMin = rows.reduce((s, r) => s + (Number(r.downtime_minutes) || 0), 0);
    const reasons = rows.map(r => r.reason_category).filter(Boolean);
    const topReason = reasons.length ? this.mode(reasons) : '-';
    const machines = new Set(rows.map(r => r.machine_id)).size;
    const boxes: InfoBox[] = [
      { title: 'Events', stat: String(rows.length), body: 'Downtime incidents' },
      { title: 'Total Downtime', stat: `${totalMin} min`, body: `~${(totalMin / 60).toFixed(1)} hours` },
      { title: 'Top Reason', stat: topReason, body: 'Most frequent category' },
      { title: 'Machines', stat: String(machines), body: 'Affected machines' },
    ];
    const charts = [
      this.countsChart('Downtime by Reason', rows.map(r => r.reason_category), 'donut'),
      this.sumByChart('Total Minutes by Machine (top 10)',
                      rows, 'machine_id', 'downtime_minutes', 10),
    ];
    return { title: 'Downtime Events', rows, columns: this.columnsOf(rows), infoBoxes: boxes, charts };
  }

  async buildCauses(): Promise<WorkspaceView> {
    const rows = await this.get('/downtime-causes');
    const cats = rows.map(r => r.category).filter(Boolean);
    const topCat = cats.length ? this.mode(cats) : '-';
    const events = new Set(rows.map(r => r.downtime_id)).size;
    const boxes: InfoBox[] = [
      { title: 'Total Causes', stat: String(rows.length), body: 'Root-cause records' },
      { title: 'Categories', stat: String(new Set(cats).size), body: `Top: ${topCat}` },
      { title: 'Events Linked', stat: String(events), body: 'Distinct events' },
      { title: 'Records', stat: String(rows.length), body: 'Cause entries' },
    ];
    const charts = [
      this.countsChart('Causes by Category', rows.map(r => r.category), 'bar'),
    ];
    return { title: 'Downtime Causes', rows, columns: this.columnsOf(rows), infoBoxes: boxes, charts };
  }

  // --- CHAT ---------------------------------------------------------------
  async sendChat(message: string): Promise<ChatResponse> {
    return await firstValueFrom(
      this.http.post<ChatResponse>(`${API}/chat`, { message })
    );
  }

  // ============================================================
  // CRUD WRAPPERS
  // ============================================================

  // Machines
  createMachine(p: any)        { return firstValueFrom(this.http.post(`${API}/machines`, p)); }
  updateMachine(id: number, p: any) { return firstValueFrom(this.http.put(`${API}/machines/${id}`, p)); }
  deleteMachine(id: number)    { return firstValueFrom(this.http.delete(`${API}/machines/${id}`)); }

  // Maintenance logs
  createMaintenance(p: any)        { return firstValueFrom(this.http.post(`${API}/maintenance-logs`, p)); }
  updateMaintenance(id: number, p: any) { return firstValueFrom(this.http.put(`${API}/maintenance-logs/${id}`, p)); }
  deleteMaintenance(id: number)    { return firstValueFrom(this.http.delete(`${API}/maintenance-logs/${id}`)); }

  // Downtime events
  createDowntime(p: any)        { return firstValueFrom(this.http.post(`${API}/downtime-events`, p)); }
  updateDowntime(id: number, p: any) { return firstValueFrom(this.http.put(`${API}/downtime-events/${id}`, p)); }
  deleteDowntime(id: number)    { return firstValueFrom(this.http.delete(`${API}/downtime-events/${id}`)); }

  // Downtime causes
  createCause(p: any)        { return firstValueFrom(this.http.post(`${API}/downtime-causes`, p)); }
  updateCause(id: number, p: any) { return firstValueFrom(this.http.put(`${API}/downtime-causes/${id}`, p)); }
  deleteCause(id: number)    { return firstValueFrom(this.http.delete(`${API}/downtime-causes/${id}`)); }



  // --- pick the builder for whichever tool the agent called ---------------
  builderForTool(toolName: string): (() => Promise<WorkspaceView>) | null {
    const map: Record<string, () => Promise<WorkspaceView>> = {
      get_all_machines: () => this.buildMachines(),
      find_machines_by_name: () => this.buildMachines(),
      add_machine: () => this.buildMachines(),
      edit_machine: () => this.buildMachines(),
      remove_machine: () => this.buildMachines(),
      get_all_maintenance_logs: () => this.buildMaintenance(),
      find_maintenance_by_machine: () => this.buildMaintenance(),
      add_maintenance_log: () => this.buildMaintenance(),
      edit_maintenance_log: () => this.buildMaintenance(),
      remove_maintenance_log: () => this.buildMaintenance(),
      get_all_downtime_events: () => this.buildDowntime(),
      find_downtime_by_machine: () => this.buildDowntime(),
      add_downtime_event: () => this.buildDowntime(),
      edit_downtime_event: () => this.buildDowntime(),
      remove_downtime_event: () => this.buildDowntime(),
      get_all_downtime_causes: () => this.buildCauses(),
      find_causes_by_downtime: () => this.buildCauses(),
      add_downtime_cause: () => this.buildCauses(),
      edit_downtime_cause: () => this.buildCauses(),
      remove_downtime_cause: () => this.buildCauses(),
    };
    return map[toolName] || null;
  }

  private mode(arr: any[]): string {
    const counts: Record<string, number> = {};
    for (const x of arr) counts[x] = (counts[x] || 0) + 1;
    let best = '-', bestN = 0;
    for (const k in counts) if (counts[k] > bestN) { best = k; bestN = counts[k]; }
    return best;
  }
  // ----- chart helpers -------------------------------------------------
  private countsChart(title: string, values: any[], type: 'donut' | 'bar') {
    const counts: Record<string, number> = {};
    for (const v of values) {
      const raw = (v ?? 'Unknown').toString().trim();
      // Title-case for consistent grouping: "running" / "RUNNING" -> "Running"
      const key = raw ? raw.charAt(0).toUpperCase() + raw.slice(1).toLowerCase() : 'Unknown';
      counts[key] = (counts[key] || 0) + 1;
    }
    return { title, type, labels: Object.keys(counts), values: Object.values(counts) };
  }

  private topCountsChart(title: string, values: any[], top: number, type: 'donut' | 'bar') {
    const c = this.countsChart(title, values, type);
    const pairs = c.labels.map((l, i) => [l, c.values[i]] as [string, number])
      .sort((a, b) => b[1] - a[1]).slice(0, top);
    return { title, type, labels: pairs.map(p => p[0]), values: pairs.map(p => p[1]) };
  }

  private sumByChart(title: string, rows: any[], keyField: string, sumField: string, top: number) {
    const sums: Record<string, number> = {};
    for (const r of rows) {
      const k = String(r[keyField] ?? 'Unknown');
      sums[k] = (sums[k] || 0) + (Number(r[sumField]) || 0);
    }
    const pairs = Object.entries(sums).sort((a, b) => b[1] - a[1]).slice(0, top);
    return {
      title, type: 'bar' as const,
      labels: pairs.map(([k]) => `Machine ${k}`),
      values: pairs.map(([, v]) => v),
    };
  }
}