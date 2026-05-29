export interface InfoBox {
  title: string;
  stat: string;
  body: string;
}

// A chart spec the component will render with ApexCharts.
export interface Chart {
  title: string;
  type: 'donut' | 'bar';
  labels: string[];
  values: number[];
}

export interface WorkspaceView {
  title: string;
  rows: any[];
  columns: string[];
  infoBoxes: InfoBox[];
  charts: Chart[];        // NEW
}

export interface ChatResponse {
  reply: string;
  tools_called: string[];
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}