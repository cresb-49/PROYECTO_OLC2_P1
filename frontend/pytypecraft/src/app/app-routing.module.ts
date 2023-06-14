import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ContainerComponent } from './components/container/container.component';
import { RouterModule, Routes } from '@angular/router';
import { HomePageComponent } from './components/home-page/home-page.component';
import { EditorComponent } from './components/editor/editor.component';
import { EditorPageComponent } from './components/editor-page/editor-page.component';
import { ReportesPageComponent } from './components/reportes-page/reportes-page.component';
import { DireccionesPageComponent } from './components/direcciones-page/direcciones-page.component';


const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'pytypecraft/home' },
  {
    path: 'pytypecraft',
    component: ContainerComponent,
    children: [
      {
        path: 'home',
        component: HomePageComponent,
      },
      {
        path: 'analisis',
        component: EditorPageComponent,
      },
      {
        path: 'reportes',
        component: ReportesPageComponent,
      },
      {
        path: 'direcciones',
        component: DireccionesPageComponent,
      }
    ],
  },
];

@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    RouterModule.forRoot(routes)
  ]
})
export class AppRoutingModule { }
