# UIKit ↔ SwiftUI Bridging Reference

## Wrapping UIKit in SwiftUI (UIViewRepresentable)

```swift
struct ActivityIndicator: UIViewRepresentable {
    let style: UIActivityIndicatorView.Style
    @Binding var isAnimating: Bool

    func makeUIView(context: Context) -> UIActivityIndicatorView {
        UIActivityIndicatorView(style: style)
    }

    func updateUIView(_ uiView: UIActivityIndicatorView, context: Context) {
        isAnimating ? uiView.startAnimating() : uiView.stopAnimating()
    }
}
```

## Wrapping SwiftUI in UIKit (UIHostingController)

```swift
// Inside a UIViewController
let swiftUIView = ProductCard(product: product, onTap: { [weak self] in
    self?.navigateToDetail()
})
let hostingController = UIHostingController(rootView: swiftUIView)
addChild(hostingController)
view.addSubview(hostingController.view)
hostingController.didMove(toParent: self)

// Constrain
hostingController.view.translatesAutoresizingMaskIntoConstraints = false
NSLayoutConstraint.activate([
    hostingController.view.topAnchor.constraint(equalTo: view.topAnchor),
    hostingController.view.leadingAnchor.constraint(equalTo: view.leadingAnchor),
    hostingController.view.trailingAnchor.constraint(equalTo: view.trailingAnchor),
    hostingController.view.bottomAnchor.constraint(equalTo: view.bottomAnchor),
])
```

## UIViewControllerRepresentable for Complex UIKit
Use when wrapping MKMapView, WKWebView, UIImagePickerController, or any
UIViewController with delegate callbacks that need Coordinator pattern.
