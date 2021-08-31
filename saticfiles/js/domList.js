const obj=
{
    "2019":
        [
            [1,2,3,4,5],[],[35],[],[],[12,55],[11,23,45],[],[],[11],[11,23],[111]
        ],
    "2020":
        [
            [1,2,3,4,5],[],[3,5,7],[],[],[12,55],[11,23,45],[],[],[11],[11,23],[111]
        ],
    "2021":
        [
            [1,2,3,4,5],[],[35],[],[],[12,11,55],[11,23,45],[],[],[11],[11,23],[111]
        ]
}
const year_no=3;
const month_no=12;
const year=new Array(2019,2020,2021);
const yearlyPostCount=new Array(15,17,16);

const month=new Array("January","February","March","April","May","June","July","August","September","October","November","December");

function dataGen(months,year){
    this.month=months;
    this.year=year;
    this.yearlyPostCount=yearlyPostCount;
}
var data=new dataGen(month,year);


function toggling(togglingNode,bolckIngElem)
{
    var toggling=document.getElementById('toggleId');
    // console.log(togglingNode.parentNode.childNodes);
    var parent=togglingNode.parentNode;
    var children=parent.childNodes;
    console.log(children);
    
    // this.len=children.length;
    if(children.length <= 4){
        console.log(children.length);
        //triggered from posts
        if(togglingNode.firstChild.className=='toogle-open'){
            togglingNode.firstChild.setAttribute('class','toogle-closed');
            togglingNode.firstChild.innerHTML="►&nbsp";
            children[3].style.display='none';
            // postAct.style.display='none';
        }
        else{
            togglingNode.firstChild.setAttribute('class','toogle-open');
            togglingNode.firstChild.innerHTML="▼&nbsp";
            children[3].style.display='block';
        }

    }
    else {
        if(togglingNode.firstChild.className=='toogle-open'){
            togglingNode.firstChild.setAttribute('class','toogle-closed');
            togglingNode.firstChild.innerHTML="►&nbsp";
            for(var bl=3;bl<children.length;bl++)
            {
                children[bl].style.display='none';
            }
        }
        else{
            togglingNode.firstChild.setAttribute('class','toogle-open');
            togglingNode.firstChild.innerHTML="▼&nbsp";
            for(var bl=3;bl<children.length;bl++)
            {
                children[bl].style.display='block';
            }
        }
    }

    
}

function toggleBlockGen(postid,filterName,postcount)
{
    var parentNode=document.createElement('ul');
    parentNode.setAttribute('class','parentElem');

    var parentExpand=document.createElement('li');
    parentExpand.setAttribute('class','parentExpanded');


    var togglingPNode=document.createElement('a');
    togglingPNode.setAttribute('class','toggle');
    togglingPNode.setAttribute('id','toggleId');
    togglingPNode.setAttribute('onclick','toggling(this)');

    var spanToggleSign=document.createElement('span');
    spanToggleSign.setAttribute('class','toogle-closed');
    spanToggleSign.innerHTML="►&nbsp";
    

    var PostFiltertType=document.createElement('a');
    PostFiltertType.setAttribute('class','postLink filterType');
    PostFiltertType.setAttribute('href','post:'+postid);
    PostFiltertType.innerHTML=filterName;

    var PostCount=document.createElement('span');
    PostCount.setAttribute('class','post-count');
    PostCount.innerHTML="&nbsp&nbsp&nbsp[&nbsp"+postcount+"&nbsp]";

    //if the parent node is for year themn we have to add again a parentNode for months.
    //if the parent Node is for month then we have to add again a childNode of postaList

    togglingPNode.appendChild(spanToggleSign);

    parentExpand.append(togglingPNode,PostFiltertType,PostCount);

    parentNode.append(parentExpand);

    return parentNode;
}

window.onload=()=>{

    console.log(obj)
    const parent=document.getElementById('testList');

    // const newBlock=toggleBlockGen('none','none','none');
    for(var yr=0;yr<data.year.length;yr++){
        const yearBlock=toggleBlockGen('none',data.year[yr],data.yearlyPostCount[yr]);
        

        for(var count=0;count<obj[data.year[yr]].length;count++)
        {
            if(obj[data.year[yr]][count].length>0)
            {       
                const newMonth=toggleBlockGen('none',data.month[count],obj[data.year[yr]][count].length);

                var monthUl=document.createElement('ul');
                
                for(let post=0;post<obj[data.year[yr]][count].length;post++){

                    var liDom=document.createElement('li');
                    var atag=document.createElement('a');
                    atag.setAttribute('href','post:'+obj[data.year[yr]][count][post]);
                    atag.innerHTML="post Title";
                    liDom.appendChild(atag);
                    monthUl.appendChild(liDom);

                }
                monthUl.style.display="none";
                newMonth.firstChild.appendChild(monthUl);
                newMonth.style.display="none";

                yearBlock.firstChild.append(newMonth);
            }
            
        }

        // yearBlock.style.display="none";

        parent.appendChild(yearBlock);

    }
    
}