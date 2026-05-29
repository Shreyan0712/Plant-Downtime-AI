import {
  Component, ElementRef, Input, OnChanges, OnDestroy, ViewChild
} from '@angular/core';
import ApexCharts from 'apexcharts';
import { Chart } from './models';

@Component({
  selector: 'app-chart-card',
  standalone: true,
  template: `
    <div class="rounded-2xl border border-[#25304a] bg-[#121a2e] p-4">
      <div class="text-sm font-semibold mb-2">{{ chart.title }}</div>
      <div #host></div>
    </div>
  `,
})
export class ChartCard implements OnChanges, OnDestroy {
  @Input({ required: true }) chart!: Chart;
  @ViewChild('host', { static: true }) host!: ElementRef<HTMLDivElement>;
  private instance?: ApexCharts;

  ngOnChanges() {
    // tear down old chart and rebuild whenever input data changes
    this.instance?.destroy();
    this.instance = new ApexCharts(this.host.nativeElement, this.buildOptions());
    this.instance.render();
  }

  ngOnDestroy() { this.instance?.destroy(); }

  private cssVar(name: string, fallback: string): string {
    if (typeof window === 'undefined') return fallback;
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim() || fallback;
  }

  private buildOptions() {
    const accent = this.cssVar('--accent', '#76ABAE');
    const text   = this.cssVar('--text', '#EEEEEE');
    const muted  = this.cssVar('--text-muted', '#b8bdc4');
    const faint  = this.cssVar('--text-faint', '#7e8590');

    // build a palette around the accent (mix in muted/faint for variation)
    // Categorical palette — distinct hues, all in the same saturation/value range
    // so they sit together visually without clashing with the theme.
    const palette = [
      '#d97757',   // copper (the theme accent, anchors the set)
      '#5b9dcc',   // muted blue
      '#85b04f',   // sage green
      '#c79553',   // amber-brown
      '#a17ec2',   // muted purple
      '#5fa19a',   // teal
      '#d18686',   // dusty rose
      '#8a92a0',   // cool gray
      '#c2a83f',   // ochre
      '#7298ad',   // steel blue
    ];

    const common = {
      chart: { type: this.chart.type, height: 420, background: 'transparent', toolbar: { show: false } },
      colors: palette,
      theme: { mode: 'dark' as const },
      legend: { labels: { colors: text } },
      dataLabels: { enabled: true },
    };
    if (this.chart.type === 'donut') {
      return {
        ...common,
        series: this.chart.values,
        labels: this.chart.labels,
        legend: { ...common.legend, position: 'bottom' as const },
        plotOptions: { pie: { donut: { size: '60%' } } },
      };
    }
    return {
      ...common,
      series: [{ name: 'Count', data: this.chart.values }],
      xaxis: {
        categories: this.chart.labels,
        labels: { style: { colors: muted }, rotate: -45, trim: true, hideOverlappingLabels: false },
      },
      yaxis: { labels: { style: { colors: muted } } },
      plotOptions: { bar: { distributed: true, columnWidth: '60%' } },
    };
  }
}