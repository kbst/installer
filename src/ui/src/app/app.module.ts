import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';

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
import { InputsComponent } from './inputs/inputs.component';
import { InputValueComponent } from './inputs/input-value.component';
import { InputValueService } from './inputs/input-value.service';

@NgModule({
  declarations: [
    AppComponent,
    ToolbarComponent,
    RunnerComponent,
    StepsComponent,
    InputsComponent,
    InputValueComponent
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
    MatStepperModule,
    ReactiveFormsModule
  ],
  providers: [
      ScenarioService,
      InputValueService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
