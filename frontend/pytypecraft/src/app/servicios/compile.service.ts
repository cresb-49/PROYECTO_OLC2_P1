import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class CompileService {
  private url = 'http://127.0.0.1:3000/compile';

  constructor(
    private http: HttpClient,
    private cookiesService: CookieService
  ) {}

  public sendCode(code: string): Observable<any> {
    let body = new Object({
      codigo: code,
    });
    return this.http.post(this.url, body);
  }
}
