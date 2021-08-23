//create two method in class render->for creating the tool UI.
//save->will extract the Block's data from that UI. 
//contenteditable is used instead input
//inlinetoolbar -->link,bold,italic

class SimpleImage{
    //for creating the toolbox set in playground
    static get toolbox(){
        return {
            title:'Image',
            icon:'<svg width="17" height="15" viewBox="0 0 336 276" xmlns="http://www.w3.org/2000/svg"><path d="M291 150V79c0-19-15-34-34-34H79c-19 0-34 15-34 34v42l67-44 81 72 56-29 42 30zm0 52l-43-30-56 30-81-67-66 39v23c0 19 15 34 34 34h178c17 0 31-13 34-29zM79 0h178c44 0 79 35 79 79v118c0 44-35 79-79 79H79c-44 0-79-35-79-79V79C0 35 35 0 79 0z"/></svg>'
        };
    }
    //create a constructor for the input data passed by user.
    constructor({data}){
        this.data=data;
        this.wrapper=undefined;
    }
    //for creating the image UI
    render(){
        this.wrapper = document.createElement('div');
        this.wrapper.classList.add('simple-image');

        if(this.data && this.data.url){
            this._createImage(this.data.url,this.data.caption);
            return this.wrapper;
        }

        const input = document.createElement('input');
    
        input.placeholder = 'Paste an image URL...';
        input.value = this.data && this.data.url ? this.data.url : '';
    
        input.addEventListener('paste', (event) => {
          this._createImage(event.clipboardData.getData('text'));
        });
    
        this.wrapper.appendChild(input);

        return this.wrapper;
      }
    //for saving the blocks content
    save(blockContent){
        const image = blockContent.querySelector('img');
        const caption = blockContent.querySelector('[contenteditable]');
      
        return {
          url: image.src,
          caption: caption.innerHTML || ''
        }
      }
    

    //for saved data validation.
    validate(savedData)
    {
        if(!savedData.url.trim()){
            return false;
        }
        return true;
    }

    //construct the method for showing the imgae

    _createImage(url, captionText){
        const image = document.createElement('img');
        const caption = document.createElement('div');
      
        image.src = url;
        caption.contentEditable = true;
        caption.innerHTML = captionText || '';
      
        this.wrapper.innerHTML = '';
        this.wrapper.appendChild(image);
        this.wrapper.appendChild(caption);
      }
      
      
}