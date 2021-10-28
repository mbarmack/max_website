import React from 'react';
import PropTypes from 'prop-types';

class Page extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            author: '',
            body: [],
            comments: [],
            created: '',
            isLoaded: false,
            logged_in: false,
            postid: '',
            title: ''
        }
        this.handleCreateComment = this.handleCreateComment.bind(this);
        this.handleDeleteComment = this.handleDeleteComment.bind(this);
    }
    handleCreateComment(author, text) {
		const requestOptions = {
			method: "POST",
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ 
                author: author,
                text: text 
            })
		}
		fetch("/api/v1/comments/?postid=" + this.state.postid, requestOptions)
			.then(response => response.json())
			.then((data) => {
				let newComment = {
					commentid: data.commentid,
					author: data.author,
                    logname_owns_this: data.logname_owns_this,
					text: data.text
				}
				let newArray = this.state.comments.concat(newComment);
				this.setState(prevState => ({
					comments: newArray
				}))
			})	
	}
    handleDeleteComment(commentid){
		const requestOptions = {
			method: "DELETE",
		}
		fetch("/api/v1/comments/"+commentid+"/", requestOptions)
			.then(
				this.setState({
					comments: this.state.comments.filter(function(comment) { 
					return comment.commentid !== commentid 
				})})
			)
	}
    componentDidMount() {
        const urlPostid = document.getElementById('react').getAttribute('data-postid');
        let url = '/api/v1/writing/' + urlPostid + '/';
        fetch(url)
            .then(res => res.json())
            .then(
                (result) => {
                this.setState({
                    author: result.author,
                    body: result.body,
                    comments: result.comments,
                    created: result.created,
                    isLoaded: true,
                    logged_in: result.logged_in,
                    postid: result.postid,
                    title: result.title
                });
                },
                (error) => {
                    this.setState({
                        isLoaded: true,
                        error
                    });
                }
            )
    }
    render() {
      const {author, body, comments, created, logged_in, title} = this.state
      const commentList = comments.map((comment) => 
        <Comment
            key={comment.commentid.toString()}
            author={comment.author}
            text={comment.text}
            lognameOwnsThis={comment.logname_owns_this}
            logged_in={logged_in}
            commentid={comment.commentid}
            handleDeleteComment={this.handleDeleteComment.bind(this)}
        />
      );

      const paragraphs = body.map((paragraph) => 
        <div key={paragraph.paragraphid} className="paragraph">
            <p>{paragraph.paragraph}</p>
        </div>
      );
      return (
          <div className="post">
              <div className="title">
                <h1>{title}</h1>
              </div>
              <div className="author">
                <h3>By {author}</h3>
              </div>
              <div className="created">
                <p>{created}</p>
              </div>
              <div className="body">
                {paragraphs}
              </div>
              <div className="comment-section">
                <CommentForm
                    logged_in={logged_in}
                    handleCreateComment={this.handleCreateComment.bind(this)}
                />
                {commentList}
              </div>
          </div>
          );
      }
  }

  class Comment extends React.Component {
      constructor(props) {
          super(props)
      }
      render() {
          return(
            <div className="comment">
                <div className="comment-author">
                    <p>{this.props.author}</p>
                </div>
                <div className="comment-text">
                    <p>{this.props.text}</p>
                </div>
                <div className="comment-delete-button">
                    <DeleteCommentButton
                        lognameOwnsThis={this.props.lognameOwnsThis}
                        logged_in={this.props.logged_in}
                        commentid={this.props.commentid}
                        handleDeleteComment={this.props.handleDeleteComment}
                    />
                </div>
            </div>
          );
      }
  }

  class CommentForm extends React.Component {
    constructor(props) {
		super(props)
		this.state = {
            author: '',
            comment: ''
        };
		this.handleInputChange = this.handleInputChange.bind(this)
		this.handleSubmit = this.handleSubmit.bind(this)
	}
	handleInputChange(event) {
        const target = event.target;
        const value = target.value
        const name = target.name;
		this.setState({
            [name]: value
        });
		event.preventDefault();
	}
	handleSubmit(event) {
		event.preventDefault();
		this.props.handleCreateComment(this.state.author, this.state.comment)
		this.setState({
            author: '',
            comment: ''
        });
	}
	render() {
        if (this.props.logged_in) {
            return(
                <form className="comment-form" onSubmit={this.handleSubmit}>
                     <label>
                        <div className="comment-input">
                            <div className="comment-input-label">
                                Name:
                            </div>
                            <input 
                                name="author"
                                type="text" 
                                value={this.state.author} 
                                onChange={this.handleInputChange} 
                            />
                        </div>
                    </label>
                    <label>
                        <div className="comment-input">
                            <div className="comment-input-label">
                                Comment:
                            </div>
                            <input 
                                name="comment"
                                type="text" 
                                value={this.state.comment} 
                                onChange={this.handleInputChange} 
                            />
                        </div>
                    </label>
                    <input className="comment-button" type="submit" value="Submit"/>
                </form>
            );
        }
        return (
            <div className="login-prompt">
                <p>Please log in to comment</p>
            </div>
        );
		
	}
  }

  class DeleteCommentButton extends React.Component {
	constructor(props) {
		super(props)
	}
	render() {
        if (this.props.logged_in) {
            if (this.props.lognameOwnsThis) {
                return (
                    <button className="delete-comment-button" onClick={ () => this.props.handleDeleteComment(this.props.commentid)}>
                        Delete Comment
                    </button>
                );
            }
        }
		return null;
	}
}


export default Page;