import { Component, OnInit, ViewChild } from '@angular/core';
import { MatStepper } from '@angular/material';

import { ScenarioService } from '../scenario.service';
import { Scenario } from '../scenario';

@Component({
  selector: 'app-runner',
  templateUrl: './runner.component.html',
  styleUrls: ['./runner.component.css']
})
export class RunnerComponent implements OnInit {
  scenario: Scenario;
  @ViewChild('stepper') stepper: MatStepper;

  constructor(private scenarioService: ScenarioService) {
      this.scenarioService = scenarioService;
  }

  ngOnInit() {
      this.scenarioService.get_scenario().subscribe(
          scenario => {
              this.scenario = scenario;
              if (scenario.status === 1) {
                  this.stepper.selectedIndex = this.stepper._steps.length - 1;
              }
          }
      );
  }

  run_scenario() {
      this.scenarioService.run().subscribe(
          scenario => {
              this.scenario = scenario;
              if (scenario.status === 0) {
                  this.scenarioService.run();
              }
          }
      );
  }

}
