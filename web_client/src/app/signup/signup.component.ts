import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, AbstractControl } from '@angular/forms';
import { matching } from './validators/matching.validator';
import { validUsername } from './validators/validUsername.validator';
import { validName } from './validators/validName.validator';
import { ApiService } from '../api.service';
import { Responses } from '../responses';
import { Router } from '@angular/router';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.scss']
})
export class SignupComponent implements OnInit {
  signupForm: FormGroup;
  submitted = false;
  isInvalid: boolean;
  rsp: boolean;

  constructor(private formBuilder: FormBuilder, private api: ApiService, private router: Router) { }

  ngOnInit() {
    this.signupForm = this.formBuilder.group({
        fullName: ['', Validators.required],
        username: ['', {
              validators : [Validators.required, Validators.minLength(3), this.getUsernameCheck.bind(this)],
              updateOn : 'blur'
        }],
        email: ['', {
          validators : [Validators.required, Validators.email, this.getEmailCheck.bind(this)],
          updateOn : 'blur'
        }],
        confirmEmail: ['', [Validators.required, Validators.email]],
        password: ['', [Validators.required, Validators.minLength(6)]],
        confirmPassword: ['', Validators.required],
        optIn: [false]
    }, {
        validator: [
          matching('password', 'confirmPassword'),
          matching('email', 'confirmEmail'),
          validUsername('username'),
          validName('fullName')
        ]
    });
  }

  get f() { return this.signupForm.controls; }

  onSubmit() {
    this.submitted = true;

    // Don't submit if invalid
    if (this.signupForm.invalid) {
      this.getRegisterAuth(this.f.fullName.value, this.f.username.value, this.f.email.value, this.f.password.value, this.f.optIn.value);
    }
  }

  getUsernameCheck(control: AbstractControl) {
    if (control.value !== '') {
      return this.api.getUsernameAvailability(control.value)
        .subscribe((data: Responses) => {
              return (data.code === 'OV0000') ? this.f.username.setErrors({ free: true }) : null;
            });
    }
  }

  getEmailCheck(control: AbstractControl) {
    if (control.value !== '') {
      this.api.getEmailAvailability(control.value)
        .subscribe((data: Responses) => {
              (data.code === 'OV0000') ? this.f.email.setErrors({ free: true }) : this.f.email.setErrors(null);
            });
    }
  }

  getRegisterAuth(name: string, user: string, email: string, pswd: string, optin: boolean) {
    if (user !== '' && pswd !== '') {
      this.api.getRegisterAuth(name, user, email, pswd, optin)
        .subscribe((data: Responses) => {
              (data.code === 'OV1111') ? this.rsp = true : this.rsp = false;
              console.log(data.code);
              this.registerAuth();
            });
    }
  }

  registerAuth() {
    (this.rsp) ? this.isInvalid = false : this.isInvalid = true;
    this.router.navigate(['/login']);
  }

}
