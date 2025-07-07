## Tasker

`post_task()`返回`Job`

`job.get()`返回`TaskDetail`

本应用的`maafw.run_ppl()`封装了`get`
```python
    b, td = maafw.run_ppl("PipelineLab20250427_Entry_01")
    print(b, td)
    print("td.status.succeeded: ", td.status.succeeded)
    print("td.status.done: ", td.status.done)
    print("td.status.failed: ",td.status.failed)
    print("td.status.pending: ", td.status.pending)
    print("td.status.running: ", td.status.running)
```
|  | `status.succeeded` | `status.done` | `status.failed` | `status.pending` | `tatus.running` |
|:-------:|:--------:|:-----------:|:----:|:----------------:|:--------------------:|
| 任务正常结束<br>`StopTask`结束<br>`post_stop()`结束 | True | True | False | False | False |
| `timeout`结束 | False | True | True | False | False |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

如果要区分一个任务链是正常结束还是`StopTask`结束的，可以让一个专门的公用节点执行`StopTask`，检查`td.nodes[-1].name`是否为停止节点。

