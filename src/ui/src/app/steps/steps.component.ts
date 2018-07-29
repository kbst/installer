import { Component, OnInit } from '@angular/core';

import { ScenarioService } from '../scenario.service';
import { Scenario } from '../scenario';

@Component({
  selector: 'app-steps',
  templateUrl: './steps.component.html',
  styleUrls: ['./steps.component.css']
})
export class StepsComponent implements OnInit {
  scenario: Scenario;
  scenarioService: ScenarioService;

  constructor(scenarioService: ScenarioService) {
      this.scenarioService = scenarioService;
  }

  ngOnInit() {
      this.scenarioService.get_scenario().subscribe(
          scenario => this.scenario = scenario
      );
  }

}
