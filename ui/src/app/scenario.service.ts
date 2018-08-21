import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { webSocket } from 'rxjs/webSocket';
import { format, parse } from 'json-rpc-protocol';

import { Scenario } from './scenario';

@Injectable({
  providedIn: 'root'
})
export class ScenarioService {
  private ws$;
  private scenario$;

  constructor() {
      const url = 'ws://localhost:4100/jsonrpc';
      this.ws$ = webSocket(url);

      this.scenario$ = new Observable<Scenario>(observer => {
          this.ws$.subscribe(
              (payload: string) => {
                observer.next(this.parse_payload(payload));
              },
              (err) => console.log(err),
              () => console.log('complete')
          );
      });
  }

  private parse_payload(payload: string) {
      let msg;
      try {
          msg = parse(payload);
      } catch (ex) {
          console.log(ex);
      }
      const scenario = new Scenario(msg.result);
      return scenario;
  }

  public get_scenario() {
      const payload = format.request(0, 'get_scenario', []);
      this.ws$.next(JSON.parse(payload));
      return this.scenario$;
  }

  public run() {
      const payload = format.request(0, 'run', []);
      this.ws$.next(JSON.parse(payload));
      return this.scenario$;
  }

  public update_inputs(scenario) {
      const payload = format.request(0, 'update_inputs', [scenario]);
      this.ws$.next(JSON.parse(payload));
      return this.scenario$;
  }

}
