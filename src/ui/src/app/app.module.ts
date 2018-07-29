import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import {
  MatButtonModule,
  MatExpansionModule,
  MatIconModule,
  MatToolbarModule,
  MatListModule,
  MatSidenavModule,
  MatStepperModule
} from '@angular/material';

import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ToolbarComponent } from './toolbar/toolbar.component';
import { RunnerComponent } from './runner/runner.component';
import { ScenarioService } from './scenario.service';
import { StepsComponent } from './steps/steps.component';

@NgModule({
  declarations: [
    AppComponent,
    ToolbarComponent,
    RunnerComponent,
    StepsComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    MatButtonModule,
    MatExpansionModule,
    MatIconModule,
    MatToolbarModule,
    MatListModule,
    MatSidenavModule,
    MatStepperModule
  ],
  providers: [
      ScenarioService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
