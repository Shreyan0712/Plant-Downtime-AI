import { Component, signal, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { WorkspaceService } from './workspace.service';
import { WorkspaceView, ChatMessage } from './models';
import { CrudForms, CrudTable } from './crud-forms';
import { ChartCard } from './chart-card';

type ViewMode = 'workspace' | 'manage';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, CrudForms, ChartCard],
  templateUrl: './app.html',
})
export class App implements OnInit {

  private ws = inject(WorkspaceService);

  view = signal<WorkspaceView | null>(null);
  messages = signal<ChatMessage[]>([]);
  draft = signal('');
  loading = signal(false);

  // view toggle
  viewMode = signal<ViewMode>('workspace');
  manageTable = signal<CrudTable>('machines');

  ngOnInit() { this.loadMachines(); }

  showWorkspace() { this.viewMode.set('workspace'); }
  manage(t: CrudTable) {
    this.manageTable.set(t);
    this.viewMode.set('manage');
  }

  async loadMachines()    { this.view.set(await this.ws.buildMachines()); }
  async loadMaintenance() { this.view.set(await this.ws.buildMaintenance()); }
  async loadDowntime()    { this.view.set(await this.ws.buildDowntime()); }
  async loadCauses()      { this.view.set(await this.ws.buildCauses()); }

  // called when a CRUD operation succeeds — refresh that table's workspace view
  async onCrudRefreshed(table: CrudTable) {
    if (table === 'machines')    this.view.set(await this.ws.buildMachines());
    if (table === 'maintenance') this.view.set(await this.ws.buildMaintenance());
    if (table === 'downtime')    this.view.set(await this.ws.buildDowntime());
    if (table === 'causes')      this.view.set(await this.ws.buildCauses());
  }

  async send() {
    const text = this.draft().trim();
    if (!text || this.loading()) return;
    this.messages.update(m => [...m, { role: 'user', content: text }]);
    this.draft.set('');
    this.loading.set(true);
    try {
      const res = await this.ws.sendChat(text);
      let builder = null;
      for (const tool of res.tools_called) {
        const b = this.ws.builderForTool(tool);
        if (b) builder = b;
      }
      if (builder) this.view.set(await builder());
      this.messages.update(m => [...m, { role: 'assistant', content: res.reply }]);
    } catch (e) {
      this.messages.update(m => [...m, { role: 'assistant', content: 'Could not reach the server.' }]);
    } finally {
      this.loading.set(false);
    }
  }
}