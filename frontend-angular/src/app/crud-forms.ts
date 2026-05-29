import { Component, Input, signal, output, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { WorkspaceService } from './workspace.service';

type Mode = 'add' | 'update' | 'delete';
export type CrudTable = 'machines' | 'maintenance' | 'downtime' | 'causes';

@Component({
  selector: 'app-crud-forms',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './crud-forms.html',
})
export class CrudForms {

  @Input({ required: true }) table!: CrudTable;

  // tells the parent when to refresh the workspace view
  refreshed = output<CrudTable>();

  private ws = inject(WorkspaceService);

  mode = signal<Mode>('add');
  busy = signal(false);
  message = signal('');           // success/error feedback under the form
  confirmDelete = signal(false);  // checkbox guard for delete

  // form model — one shared object, fields used depend on which table
  form: any = {};
  // for update/delete we also need the id
  recordId: number | null = null;

  setMode(m: Mode) {
    this.mode.set(m);
    this.message.set('');
    this.form = {};
    this.recordId = null;
    this.confirmDelete.set(false);
  }

  async submit() {
    this.busy.set(true);
    this.message.set('');
    try {
      const payload = this.cleanPayload(this.form);
      let result: any;

      if (this.mode() === 'add') {
        result = await this.create(payload);
      } else if (this.mode() === 'update') {
        if (!this.recordId) { this.message.set('Please provide an ID.'); return; }
        result = await this.update(this.recordId, payload);
      } else if (this.mode() === 'delete') {
        if (!this.recordId) { this.message.set('Please provide an ID.'); return; }
        if (!this.confirmDelete()) { this.message.set('Tick the confirmation box first.'); return; }
        result = await this.remove(this.recordId);
      }

      this.message.set('Done.');
      this.form = {};
      this.recordId = null;
      this.confirmDelete.set(false);
      // tell parent to refresh the workspace table for this resource
      this.refreshed.emit(this.table);
    } catch (e: any) {
      this.message.set(`Error: ${e?.error?.detail ?? e?.message ?? 'request failed'}`);
    } finally {
      this.busy.set(false);
    }
  }

  // strip empty strings/nulls so PUT doesn't overwrite fields the user didn't fill
  private cleanPayload(obj: any) {
    const out: any = {};
    for (const k of Object.keys(obj)) {
      const v = obj[k];
      if (v !== '' && v !== null && v !== undefined) out[k] = v;
    }
    return out;
  }

  private create(p: any) {
    switch (this.table) {
      case 'machines':    return this.ws.createMachine(p);
      case 'maintenance': return this.ws.createMaintenance(p);
      case 'downtime':    return this.ws.createDowntime(p);
      case 'causes':      return this.ws.createCause(p);
    }
  }
  private update(id: number, p: any) {
    switch (this.table) {
      case 'machines':    return this.ws.updateMachine(id, p);
      case 'maintenance': return this.ws.updateMaintenance(id, p);
      case 'downtime':    return this.ws.updateDowntime(id, p);
      case 'causes':      return this.ws.updateCause(id, p);
    }
  }
  private remove(id: number) {
    switch (this.table) {
      case 'machines':    return this.ws.deleteMachine(id);
      case 'maintenance': return this.ws.deleteMaintenance(id);
      case 'downtime':    return this.ws.deleteDowntime(id);
      case 'causes':      return this.ws.deleteCause(id);
    }
  }
}