var member = []
var lottery_cfg = []

fetch('/api/get_lottery_info', {
    method: "POST",
    body: "",
    headers: {
        "Content-type": "application/x-www-form-urlencoded"
    }
})
.then(response => response.json())
.then(data =>{
    member = data['data']['lottery_person']
    lottery_cfg = data['data']['lottery_cfg']
    console.log(lottery_cfg)
    init()
});