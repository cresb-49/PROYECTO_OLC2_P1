import { AfterViewInit, Component } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';

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

  constructor(private cookieService:CookieService) {
    
  }

  ngAfterViewInit(): void {
    if (this.cookieService.check('compile')) {
      this.setTablaSimbolos();
    }
  }

  public setTablaSimbolos(): void {
    let simbolos = JSON.parse(this.cookieService.get('compile')).simbolos;
    this.dataSource = simbolos;
  }
}
