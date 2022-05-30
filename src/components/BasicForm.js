import { useState } from "react";

const BasicForm = (props) => {
  const [enteredFirstName, setEnteredFirstName] = useState("");
  const [enteredLastName, setEnteredLastName] = useState("");
  const [enteredEmail, setEnteredEmail] = useState("");
  const [firstNameIsValid, setFirstNameIsValid] = useState(false);
  const [lastNameIsValid, setLastNameIsValid] = useState(false);
  const [emailIsValid, setEmailIsValid] = useState(false);
  const [firstNameIsTouched, setFirstNameIsTouched] = useState(false);
  const [lastNameIsTouched, setLastNameIsTouched] = useState(false);
  const [emailIsTouched, setEmailIsTouched] = useState(false);

  const firstNameInputIsInValid = !firstNameIsValid && firstNameIsTouched;
  const lastNameInputIsInValid = !lastNameIsValid && lastNameIsTouched;
  const emailInputIsInValid = !emailIsValid && emailIsTouched;

  const firstNameChangeHandler = (event) => {
    setFirstNameIsTouched(true);
    setEnteredFirstName(event.target.value);

    if (event.target.value.trim() !== "") {
      setFirstNameIsValid(true);
    }
  };

  const firstNameBlurHandler = () => {
    if (enteredFirstName.trim() === "") {
      setFirstNameIsValid(false);
    }
  };

  const lastNameChangeHandler = (event) => {
    setLastNameIsTouched(true);
    setEnteredLastName(event.target.value);
    if (event.target.value.trim() !== "") {
      setLastNameIsValid(true);
    }
  };

  const lastNameBlurHandler = () => {
    if (enteredLastName.trim() === "") {
      setLastNameIsValid(false);
    }
  };

  const emailChangeHandler = (event) => {
    setEmailIsTouched(true);
    setEnteredEmail(event.target.value);
    if (event.target.value.includes("@") && event.target.value.trim() !== "") {
      setEmailIsValid(true);
    } else {
      setEmailIsValid(false);
    }
  };

  const emailBlurHandler = () => {
    if (!enteredEmail.includes("@") && enteredEmail.trim() === "") {
      setEmailIsValid(false);
    }
  };

  let formIsValid = false;
  if (firstNameIsValid && lastNameIsValid && emailIsValid) {
    formIsValid = true;
  }

  const formSubmitHandler = (event) => {
    event.preventDefault();

    setEnteredFirstName("");
    setEnteredLastName("");
    setEnteredEmail("");
  };

  const firstNameValidClasses = firstNameInputIsInValid
    ? "form-control invalid"
    : "form-control";
  const lastNameValidClasses = lastNameInputIsInValid
    ? "form-control invalid"
    : "form-control";
  const emailValidClasses = emailInputIsInValid
    ? "form-control invalid"
    : "form-control";

  return (
    <form onSubmit={formSubmitHandler}>
      <div className="control-group">
        <div className={firstNameValidClasses}>
          <label htmlFor="name">First Name</label>
          <input
            type="text"
            id="name"
            onChange={firstNameChangeHandler}
            onBlur={firstNameBlurHandler}
            value={enteredFirstName}
          />
          {firstNameInputIsInValid && (
            <p className="error-text">First name should not be empty</p>
          )}
        </div>
        <div className={lastNameValidClasses}>
          <label htmlFor="name">Last Name</label>
          <input
            type="text"
            id="name"
            onChange={lastNameChangeHandler}
            onBlur={lastNameBlurHandler}
            value={enteredLastName}
          />
          {lastNameInputIsInValid && (
            <p className="error-text">Last name should not be empty</p>
          )}
        </div>
      </div>
      <div className={emailValidClasses}>
        <label htmlFor="name">E-Mail Address</label>
        <input
          type="text"
          id="name"
          onChange={emailChangeHandler}
          onBlur={emailBlurHandler}
          value={enteredEmail}
        />
        {emailInputIsInValid && <p className="error-text">Not valid Email</p>}
      </div>
      <div className="form-actions">
        <button disabled={!formIsValid}>Submit</button>
      </div>
    </form>
  );
};

export default BasicForm;
