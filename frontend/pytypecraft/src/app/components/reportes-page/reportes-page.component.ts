import { AfterViewInit, Component } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { graphviz } from 'd3-graphviz';

@Component({
  selector: 'app-reportes-page',
  templateUrl: './reportes-page.component.html',
  styleUrls: ['./reportes-page.component.css'],
})
export class ReportesPageComponent implements AfterViewInit {
  displayedColumns: string[] = [
    'nombre',
    'tipo',
    'clase',
    'ambito',
    'linea',
    'columna',
  ];

  dataSource = [];

  constructor(private cookieService: CookieService) {}

  ngAfterViewInit(): void {
    if (localStorage.getItem('compile') != null) {
      this.setTablaSimbolos();
      this.setImg();
    }
  }

  public setTablaSimbolos(): void {
    let simbolos = JSON.parse(localStorage.getItem('compile')!).simbolos;
    this.dataSource = simbolos;
  }

  public setImg(): void {
    let dot = JSON.parse(localStorage.getItem('compile')!).dot;
    graphviz('#graph').width(1200).height(500).fit(true).renderDot(dot);
  }
}
