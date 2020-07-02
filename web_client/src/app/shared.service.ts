import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable()
export class SharedService {

  private username = new BehaviorSubject('');
  private email = new BehaviorSubject('');

  getUsername = this.username.asObservable();
  getEmail = this.email.asObservable();

  constructor() { }

  setUsername(user: string) {
    this.username.next(user);
  }

  setEmail(email: string) {
    this.email.next(email);
  }
}
