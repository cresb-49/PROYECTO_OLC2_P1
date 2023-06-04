import { Component, ViewChild } from '@angular/core';
import { EditorComponent } from '../editor/editor.component';

@Component({
  selector: 'app-editor-page',
  templateUrl: './editor-page.component.html',
  styleUrls: ['./editor-page.component.css']
})
export class EditorPageComponent {
  @ViewChild('consoleResult') resultConsole!:EditorComponent;

}
