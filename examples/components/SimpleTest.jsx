function SimpleTest(props) {
    var message = props.message || 'Hello World';
    
    return React.createElement('div', {
        style: {
            padding: '20px',
            backgroundColor: '#f0f0f0',
            border: '1px solid #ccc',
            borderRadius: '5px'
        }
    }, [
        React.createElement('h1', null, 'Simple Test Component'),
        React.createElement('p', null, message)
    ]);
}
