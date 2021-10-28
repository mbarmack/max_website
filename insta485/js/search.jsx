import React from 'react';
import PropTypes from 'prop-types';

class Search extends React.Component {
    constructor(props) {
        super(props);
        this.handleChange = this.handleChange.bind(this);
        this.state = {
            url: '/api/v1/writing/?search=',
            posts: [],
            filterValue: ''
        }
    }
    fetchPosts() {
        let url = this.state.url;

        fetch(url)
        .then(response => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
        })
        .then((data) => {
            this.setState({
                posts: data.posts
            })
        })
    }
    handleChange(value) {
        this.setState({
            filterValue: value
        })
    }
    componentDidMount() {
        this.fetchPosts();
    }
    render() {
        const {posts, filterValue} = this.state;
        const postList = [];
        posts.forEach((post) => {
            let title = post.title.toLowerCase();
            let filter = filterValue.toLowerCase();
            if (title.indexOf(filter) === -1) {
              return;
            }
            postList.push(
                <ul key={post.postid}>
                    <WritingPost
                        post={post}
                    />
                </ul>
            );
          });
        return (
            <div className="writing-content">
                <SearchBar
                    handleChange={this.handleChange}
                />
                <div className="search-results">
                    {postList}
                </div>
            </div>
        );
    }
}

class SearchBar extends React.Component {
    constructor(props) {
        super(props)
        this.handleChange = this.handleChange.bind(this);
    }
    handleChange(e) {
        this.props.handleChange(e.target.value);
    }
    render() {
        return (
            <form className="search-bar">
                    <input 
                        className="search-input"
                        type="text" 
                        value={this.props.filterValue} 
                        onChange={this.handleChange}
                        placeholder="Search..."
                    />
            </form>
        );
    }
}

class WritingPost extends React.Component {
    constructor(props) {
        super(props);
    }
    render() {
        const {postid, title, author} = this.props.post;
        return(
            <div className="writing_post">
                <a href={`/writing/${postid}/`}>{title}</a>
                <p>{`By ${author}`}</p>
            </div>
        );
    }
}

export default Search;