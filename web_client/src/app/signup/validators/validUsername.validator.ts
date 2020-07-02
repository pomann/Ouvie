import { FormGroup } from '@angular/forms';


export function validUsername(matchOne: string) {
    return (formGroup: FormGroup) => {
        const varOne = formGroup.controls[matchOne];

        if (varOne.errors) {
            return;
        }

        if (!varOne.value.match(/^[a-z0-9]+$/i)) {
            varOne.setErrors({ valid: true });
        } else {
            varOne.setErrors(null);
        }
    };
}
