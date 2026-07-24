# Core Data & SwiftData Persistence Guide

## SwiftData (iOS 17+) — Preferred for New Apps

```swift
@Model
final class TaskItem {
    var title: String
    var dueDate: Date?
    var isCompleted: Bool
    @Relationship(deleteRule: .cascade) var subtasks: [Subtask]

    init(title: String, dueDate: Date? = nil) {
        self.title = title
        self.dueDate = dueDate
        self.isCompleted = false
        self.subtasks = []
    }
}

// Usage in SwiftUI
struct TaskListView: View {
    @Query(sort: \TaskItem.dueDate) private var tasks: [TaskItem]
    @Environment(\.modelContext) private var modelContext

    var body: some View {
        List(tasks) { task in
            TaskRow(task: task)
        }
    }
}
```

## Core Data (iOS 16-) — NSPersistentContainer

```swift
final class PersistenceController {
    static let shared = PersistenceController()
    let container: NSPersistentContainer

    init(inMemory: Bool = false) {
        container = NSPersistentContainer(name: "AppModel")
        if inMemory {
            container.persistentStoreDescriptions.first?.url = URL(fileURLWithPath: "/dev/null")
        }
        container.loadPersistentStores { _, error in
            if let error = error { fatalError("Core Data store failed: \(error)") }
        }
        container.viewContext.automaticallyMergesChangesFromParent = true
    }
}
```

## Migration Strategy
- Lightweight: Set `NSMigratePersistentStoresAutomaticallyOption` and `NSInferMappingModelAutomaticallyOption`
- Heavy: Use `NSMappingModel` + custom `NSEntityMigrationPolicy`
