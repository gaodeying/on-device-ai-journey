#include <iostream>
#include <memory>
#include <utility> // std::move
#include <functional>

struct Foo {
    Foo() { std::cout << "Foo::Foo" << std::endl; }
    ~Foo() { std::cout << "Foo::~Foo" << std::endl; }
    void foo() { std::cout << "Foo::foo" << std::endl; }
};

void f(const Foo &) {
    std::cout << "f(const Foo&)" << std::endl;
}

void lambda_expression_capture() {
    auto important = std::make_unique<int>(1);
    auto add = [v1 = 1, v2 = std::move(important)](int x, int y) -> int {
        return x+y+v1+(*v2);
    };
    std::cout << "lamda gaoooo" << std::endl;
    std::cout << add(3,4) << std::endl;
}

int foo(int para) {
    return para;
}

void functionTest() {
    // std::function 包装了一个返回值为 int, 参数为 int 的函数
    std::function<int(int)> func = foo;

    int important = 10;
    std::function<int(int)> func2 = [&](int value) -> int {
        return 1+value+important;
    };
    std::cout << func(10) << std::endl;
    std::cout << func2(10) << std::endl;
}

void demo_lambda() {
    std::cout << "/n ===== lambda =====" << std::endl;

    auto add = [](int a, int b) { return a + b; };
    std::cout << " add(3, 4) = " << add(3, 4) << std::endl;

    int inference_count = 0;
    auto logger = [&inference_count](const std::string & msg) {
        inference_count ++;
        std::cout << " [Inference #" << inference_count << "]" << msg << std::endl;
    };

    logger("开始推理...");
    logger("推理结束");

    // std::function<void(const std::string&)> callback = logger;
    // 这里加&（即&logger）是因为logger是一个捕获了局部变量的lambda，直接赋值给std::function时编译器允许转换，
    // 但如果logger是mutable lambda或希望保持引用而非拷贝，可以写成std::function<void(const std::string&)> callback = std::ref(logger);
    // 实际上，std::function会拷贝logger，不用&也行，但如果传递的是可变lambda或需要保持捕获变量同步，需要std::ref或&。
    std::function<void(const std::string&)> callback = logger;
    callback("通过 function 调用");

}

void fooTest() {
    std::unique_ptr<Foo> p1(std::make_unique<Foo>());
    // p1 不空, 输出
    if (p1) p1->foo();
    {
        std::unique_ptr<Foo> p2(std::move(p1));
        // p2 不空, 输出
        f(*p2);
        // p2 不空, 输出
        if(p2) p2->foo();
        // p1 为空, 无输出
        if(p1) p1->foo();
        p1 = std::move(p2);
        // p2 为空, 无输出
        if(p2) p2->foo();
        std::cout << "p2 被销毁" << std::endl;
    }
    // p1 不空, 输出
    if (p1) p1->foo();
    // Foo 的实例会在离开作用域时被销毁
}

int main() {
    
    // lambda_expression_capture();

    // std::cout << "Funtion Test" << std::endl;

    // functionTest();

    demo_lambda();
}




