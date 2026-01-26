---
name: forms-validation
description: Form libraries (React Hook Form, Formik), validation schemas (Zod, Yup), file uploads, multi-step forms, and form accessibility. Use when building forms, implementing validation, handling file uploads, or creating wizard flows.
---

# Forms & Validation

Build robust, user-friendly forms with validation.

## 1. React Hook Form

### Basic Form
```typescript
import { useForm } from 'react-hook-form';

interface FormData {
  email: string;
  password: string;
}

function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>();
  
  const onSubmit = (data: FormData) => {
    console.log(data);
  };
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input
        {...register('email', {
          required: 'Email is required',
          pattern: {
            value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
            message: 'Invalid email address'
          }
        })}
        type="email"
      />
      {errors.email && <span role="alert">{errors.email.message}</span>}
      
      <input
        {...register('password', {
          required: 'Password is required',
          minLength: {
            value: 8,
            message: 'Password must be at least 8 characters'
          }
        })}
        type="password"
      />
      {errors.password && <span role="alert">{errors.password.message}</span>}
      
      <button type="submit">Login</button>
    </form>
  );
}
```

## 2. Zod Validation

```typescript
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';

const userSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  age: z.number().min(18, 'Must be 18 or older'),
  terms: z.boolean().refine(val => val === true, 'Must accept terms')
});

type UserFormData = z.infer<typeof userSchema>;

function UserForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<UserFormData>({
    resolver: zodResolver(userSchema)
  });
  
  return (
    <form onSubmit={handleSubmit(data => console.log(data))}>
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}
      
      <input {...register('password')} type="password" />
      {errors.password && <span>{errors.password.message}</span>}
      
      <input {...register('age', { valueAsNumber: true })} type="number" />
      {errors.age && <span>{errors.age.message}</span>}
      
      <input {...register('terms')} type="checkbox" />
      {errors.terms && <span>{errors.terms.message}</span>}
      
      <button type="submit">Submit</button>
    </form>
  );
}
```

## 3. File Uploads

```typescript
function FileUpload() {
  const { register, handleSubmit, watch } = useForm();
  const file = watch('file')?.[0];
  
  // Preview
  const [preview, setPreview] = useState<string>();
  
  useEffect(() => {
    if (!file) return;
    const url = URL.createObjectURL(file);
    setPreview(url);
    return () => URL.revokeObjectURL(url);
  }, [file]);
  
  const onSubmit = async (data: any) => {
    const formData = new FormData();
    formData.append('file', data.file[0]);
    
    await fetch('/api/upload', {
      method: 'POST',
      body: formData
    });
  };
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input
        {...register('file', { required: true })}
        type="file"
        accept="image/*"
      />
      {preview && <img src={preview} alt="Preview" />}
      <button type="submit">Upload</button>
    </form>
  );
}

// Drag & Drop
function DragDropUpload() {
  const [isDragging, setIsDragging] = useState(false);
  
  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const files = Array.from(e.dataTransfer.files);
    handleFiles(files);
  };
  
  return (
    <div
      onDrop={handleDrop}
      onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
      onDragLeave={() => setIsDragging(false)}
      className={isDragging ? 'border-blue-500' : 'border-gray-300'}
    >
      Drop files here
    </div>
  );
}
```

## 4. Multi-Step Forms

```typescript
function MultiStepForm() {
  const [step, setStep] = useState(1);
  const { register, handleSubmit, trigger } = useForm();
  
  const nextStep = async () => {
    const isValid = await trigger(); // Validate current step
    if (isValid) setStep(step + 1);
  };
  
  return (
    <form onSubmit={handleSubmit(data => console.log(data))}>
      {step === 1 && (
        <div>
          <h2>Step 1: Personal Info</h2>
          <input {...register('name', { required: true })} />
          <input {...register('email', { required: true })} />
          <button type="button" onClick={nextStep}>Next</button>
        </div>
      )}
      
      {step === 2 && (
        <div>
          <h2>Step 2: Address</h2>
          <input {...register('street', { required: true })} />
          <input {...register('city', { required: true })} />
          <button type="button" onClick={() => setStep(1)}>Back</button>
          <button type="button" onClick={nextStep}>Next</button>
        </div>
      )}
      
      {step === 3 && (
        <div>
          <h2>Step 3: Review</h2>
          {/* Show summary */}
          <button type="button" onClick={() => setStep(2)}>Back</button>
          <button type="submit">Submit</button>
        </div>
      )}
    </form>
  );
}
```

## 5. Dynamic Fields

```typescript
import { useFieldArray } from 'react-hook-form';

function DynamicForm() {
  const { register, control } = useForm({
    defaultValues: {
      items: [{ name: '', quantity: 0 }]
    }
  });
  
  const { fields, append, remove } = useFieldArray({
    control,
    name: 'items'
  });
  
  return (
    <form>
      {fields.map((field, index) => (
        <div key={field.id}>
          <input {...register(`items.${index}.name`)} />
          <input {...register(`items.${index}.quantity`)} type="number" />
          <button type="button" onClick={() => remove(index)}>Remove</button>
        </div>
      ))}
      <button type="button" onClick={() => append({ name: '', quantity: 0 })}>
        Add Item
      </button>
    </form>
  );
}
```

## 6. Accessible Forms

```typescript
function AccessibleForm() {
  const { register, formState: { errors } } = useForm();
  
  return (
    <form>
      <div>
        <label htmlFor="email">
          Email <span aria-label="required">*</span>
        </label>
        <input
          id="email"
          {...register('email', { required: 'Email is required' })}
          aria-required="true"
          aria-invalid={errors.email ? 'true' : 'false'}
          aria-describedby={errors.email ? 'email-error' : undefined}
        />
        {errors.email && (
          <span id="email-error" role="alert" className="error">
            {errors.email.message}
          </span>
        )}
      </div>
    </form>
  );
}
```

## Best Practices

1. **Use React Hook Form** - Better performance than controlled forms
2. **Validate with Zod** - Type-safe validation schemas
3. **Accessible labels** - Always associate labels with inputs
4. **Clear error messages** - Tell users what's wrong and how to fix
5. **Validate on blur** - Don't interrupt typing
6. **Show success states** - Positive feedback
7. **Disable submit while submitting** - Prevent double submission
8. **Save progress** - For long forms, save to localStorage
