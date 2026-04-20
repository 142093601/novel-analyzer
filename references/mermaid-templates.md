# Mermaid Graph Templates

## Character Relationship Graph

```mermaid
graph TD
    A[角色A] -->|同盟| B[角色B]
    A -->|对立| C[角色C]
    B -->|师徒| D[角色D]
    C -->|暧昧| A
    D -->|血缘| B
```

## Relationship Line Styles

- Solid line `-->`: Strong bond (family, deep friendship, romance)
- Dashed line `-.->`: Weak or temporary bond (alliance of convenience)
- Thick line `==>`: Critical relationship (main antagonist, true love)

## Relationship Labels

| Chinese | English | Mermaid Label |
|---------|---------|---------------|
| 同盟 | Ally | 同盟 |
| 对立 | Antagonist | 对立 |
| 师徒 | Mentor | 师徒 |
| 爱情 | Romance | ❤️ |
| 血缘 | Family | 血缘 |
| 利益 | Transactional | 利益 |
| 亦敌亦友 | Frenemy | 亦敌亦友 |

## Plot Timeline

```mermaid
timeline
    title 剧情时间线
    第一卷 开端
        : 事件A
        : 事件B
    第二卷 发展
        : 事件C
        : 事件D
    第三卷 高潮
        : 事件E
```
