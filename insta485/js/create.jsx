import React from 'react';

class Create extends React.Component{
    constructor(props) {
        super(props)
        this.state = {
            usernames: [],
            password1: '',
            password2: ''
        }
    }
    componentDidMount() {
        const requestOptions = {
			method: "POST",
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ 
                sender: "admin",
                key: "gh576nl5ttn9i" 
            })
		}
        fetch('/api/v1/users/', requestOptions)
        .then(response => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
        })
        .then((data) => {
            this.setState({
                usernames: data.users
            })
        })
    }
    render() {
        const { usernames, password1, password2 } = this.state;
        return(
            <div className="form-inputs">
                <Username
                    usernames={usernames}
                />
                <Passwords/>
            </div>
        );
    }
}

class Username extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            unique: true
        }
        this.handleChange = this.handleChange.bind(this);
    }
    handleChange(e) {
        const value = e.target.value;
        const usernames = this.props.usernames;
        let isUnique = true;
        for (let i=0; i< usernames.length; ++i) {
            if (usernames[i].username.toLowerCase() === value.toLowerCase()) {
                isUnique = false;
                break;
            }
        }
        if(isUnique) {
            this.setState({ unique: true })
        } else {
            this.setState({ unique: false })
        }
    }
    render() {
        return (
            <div className="create-username">
                <div className="create-input-label">
                    Username
                </div>
                <div className="username-taken">
                    {this.state.unique ? "" : "Username taken"}
                </div>
                <input type="text" name="username" onChange={this.handleChange} required/>
            </div>
        );
    }
}

class Passwords extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            password: '',
            password2: ''
        }
        this.handleChange = this.handleChange.bind(this);
    }
    handleChange(e) {
        const target = e.target;
        const value = target.value
        const name = target.name;
		this.setState({
            [name]: value
        });
		e.preventDefault();
    }
    render() {
        let passwordsMatch = (this.state.password === this.state.password2);
        return(
           <div className="create-password">
               <div className="create-input-label">
                    Password
                </div>
                <input type="password" name="password" onChange={this.handleChange} required/>
                <div className="create-input-label">
                    Confirm Password
                </div>
                <input type="password" name="password2" onChange={this.handleChange} required/>
                <div className="password-match">
                    {passwordsMatch ? "" : "Passwords must match"}
                </div>
           </div> 
        );
    }
}

export default Create;